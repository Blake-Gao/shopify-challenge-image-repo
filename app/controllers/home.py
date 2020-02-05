from flask import Flask, Blueprint, render_template, request

import boto3

blueprint = Blueprint('home', __name__)
app = Flask(__name__)

def get_images_in_folder(dir):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket("bgao-shopfiy-images")
    location = boto3.client('s3').get_bucket_location(Bucket="bgao-shopfiy-images")['LocationConstraint']
    images = []
    for i, image in enumerate(bucket.objects.filter(Prefix=dir)):
        if image.key[-1] != "/":
            url = "https://s3-%s.amazonaws.com/%s/%s" % (location, image.bucket_name, image.key)
            images.append({"id": i, "src": url})

    return images

@blueprint.route('/purchase', methods=['POST'])
def purchase():
    from app.app import get_cursor
    cur, conn = get_cursor()

    image_src = request.form.get('src')
    cur.execute("""INSERT INTO purchase (src, price) VALUES (?, ?)""", (image_src, 100))
    conn.commit()

    return render_template('home/purchase.html', image_src=image_src)


@blueprint.route('/')
def index():
    from app.app import get_cursor
    cur, conn = get_cursor()
    cur.execute("SELECT rowid, * FROM purchase")
    purchase_db_rows = cur.fetchall()
    purchases = []
    total_spent = 0

    for row in purchase_db_rows:
        total_spent += int(row[2])
        purchases.append({"id": row[0], "src": row[1]})

    inventory = get_images_in_folder("inventory")
    sold = get_images_in_folder("sold")

    return render_template('home/index.html', inventory=inventory, purchases=purchases, sold=sold, total_spent=total_spent)
