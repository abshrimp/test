from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv

start = time.time()

URL = "https://www.google.com/maps/"

options = Options()
options.add_argument("--headless")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--no-sandbox")
options.add_argument("--lang=ja")

driver = webdriver.Chrome(options=options)

driver.get(URL)
time.sleep(3)
driver.find_element(By.CSS_SELECTOR, "form").submit()
time.sleep(3)
driver.execute_script("""
window.get2 = function(x, y, z, x2, y2) {
    var lat = 180 * (x * 256 / 2 ** (z + 7) - 1);
    var lat2 = 180 * ((x + 1) * 256 / 2 ** (z + 7) - 1) - lat;
    lat += lat2 / 256 * (x2 + 0.5);
    var lng = 180 / Math.PI * Math.asin(Math.tanh(-Math.PI / 2 ** (z + 7) * y * 256 + Math.atanh(Math.sin(Math.PI / 180 * 85.05112878))));
    var lng2 = 180 / Math.PI * Math.asin(Math.tanh(-Math.PI / 2 ** (z + 7) * (y + 1) * 256 + Math.atanh(Math.sin(Math.PI / 180 * 85.05112878)))) - lng;
    lng += lng2 / 256 * (y2 + 0.5);
    return [lat, lng]
}
window.zindex = 11;
window.out = [];
window.out2 = [];
window.count2 = 0;
window.x3 = 1723;
window.y3 = 732;
window.loop = async function() {
    for (y3 = 732; y3 <= 732; y3++) {
        for (x3 = 1723; x3 <= 1853; x3++) {
            await loop2(x3, y3)
        }
    }
}
window.loop2 = async function(x, y) {
    return new Promise(resolve => {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "https://cyberjapandata.gsi.go.jp/xyz/dem/" + zindex + "/" + x + "/" + y + ".txt");
        xhr.onreadystatechange = async function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    var arr = xhr.responseText.split("\\n");
                    let count = 0;
                    count2 = 0;
                    for (let i = 0; i < arr.length; i++) {
                        arr[i] = arr[i].split(",");
                        for (let j = 0; j < arr[i].length; j++) {
                            if (arr[i][j] != "e") {
                                let point = get2(x, y, zindex, i, j);
                                setTimeout(function() {
                                    loop3(point);
                                }, count * 3);
                                count++;
                            }
                        }
                    }
                    let timer = setInterval(function(){
                        if (count == count2) {
                            clearInterval(timer);
                            console.log(x)
                            resolve();
                        }
                    }, 10)
                } else resolve();
            }
        }
        xhr.send();
    });
}
window.loop3 = function(point) {
        var xhr2 = new XMLHttpRequest();
        xhr2.open("GET", "https://www.google.com/maps/rpc/photo/listentityphotos?authuser=0&hl=ja&gl=jp&pb=!1e3!5m54!2m2!1i203!2i100!3m3!2i4!3sCAEIBAgFCAYgAQ!5b1!7m42!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!8m0!9b0!11m1!4b1!6m3!1syc5GZtC5CKDm1e8Pvfq1sAQ!7e81!15i11021!9m2!2d" + point[0] + "!3d" + point[1] + "!10d25");
        xhr2.onreadystatechange = function () {
            if (xhr2.readyState === 4) {
                count2++;
                if (xhr2.status === 200) {
                    var arr = JSON.parse(xhr2.responseText.replace(")]}'", ""))[0];
                    if (arr === null) {
                        return;
                    }
                    for (let i = 0; i < arr.length; i++) {
                        if (arr[i][0].length == 22 && !out2.includes(arr[i][0])) {
                            out.push([arr[i][0], arr[i][8][0][1], arr[i][8][0][2]]);
                            out2.push(arr[i][0]);
                        }
                    }
                }
            }
        }
        xhr2.send();
}
loop();
""")
y2 = 732
x2 = 0
while(time.time() - start < 19800):
  logs = driver.get_log("browser")
  for log in logs:
    print(log)
  x = driver.execute_script("return x3")
  y = driver.execute_script("return y3")
  if (x2 != x):
    x2 = x
    print(str(x) + " " + str(y))
    out = driver.execute_script("return out")
    csv_path = r"out.csv"
    with open(csv_path, 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerows(out)
  if (y2 != y):
      break
  time.sleep(3)
driver.quit()
