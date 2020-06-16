from flask import Flask, escape, request
from main import get_bucket, gen_signed_url
import urllib

app = Flask(__name__)


@app.route('/')
def index():
    objname = request.args.get("n", "")
    objname = escape(objname)
    if not objname:
        return "Wuz up?"
    bucket = get_bucket()
    _, short_url, _ = gen_signed_url(bucket, objname)
    html_template = r"""
    <!DOCTYPE html>
    <html>
    <body>

    <input type="text" value="
    """ + short_url + r"""
    " id="myInput">
    <button onclick="myFunction()">Copy</button>

    <script>
    function myFunction() {
    var copyText = document.getElementById("myInput");
    copyText.select();
    copyText.setSelectionRange(0, 99999)
    document.execCommand("copy");
    alert("Copied the text: " + copyText.value);
    }
    </script>

    </body>
    </html>
    """
    return html_template
