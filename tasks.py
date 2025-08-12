from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """

    browser.configure(slowmo=800)

    # open_robot_order_website()
    # get_orders()
    # give_up_consitutional_rights()
    # order_all()
    archieve_receipts()


def open_robot_order_website():
    browser.goto("https://robotsparebinindustries.com/#/robot-order")


def get_orders():
    http = HTTP()
    return http.download("https://robotsparebinindustries.com/orders.csv", overwrite=True)


def make_table():
    table = Tables()
    return table.read_table_from_csv("orders.csv", header=True)


def give_up_consitutional_rights():
    page = browser.page()
    page.click("text=OK")


def fill_form(order):
    page = browser.page()

    page.select_option("#head", str(order["Head"]))
    page.click(f"input#id-body-{str(order['Body'])}")
    page.fill("input[placeholder='Enter the part number for the legs']", str(order["Legs"]))
    page.fill("input[placeholder='Shipping address']", str(order["Address"]))

    page.click("#order")

    error_check()
    take_screenshot(page, str(order["Order number"]))
    store_pdf_as_receipt(order)
    
    page.click("text=Order another robot")
    
    page.click("text=OK")

def store_pdf_as_receipt(order):
    
    pdf = PDF()
    html_content = f"""
        
            <h1>   
                <font color="black", face="Courier">
                Receipt #{order["Order number"]}
                </font>
            </h1>
        <center>
        <img src="output/receipts/order {order["Order number"]}.png" width="550">
        </center>
        """

    pdf.html_to_pdf(html_content, f"output/receipts/receipt {order["Order number"]}.pdf")
    

def take_screenshot(page, order_number):
    page.screenshot(path=f"output/receipts/order {order_number}.png")

def order_all():
    table = make_table()

    for row in table:
        fill_form(row)

def error_check():
    page = browser.page()
    if page:
        if page.locator("div.alert.alert-danger").is_visible():
            page.click("#order")
            error_check()
    else:
        pass

def archieve_receipts():
    lib = Archive()
    lib.archive_folder_with_zip(folder="output/receipts", archive_name="output/receipt archieve.zip", recursive=False, include="*.pdf")