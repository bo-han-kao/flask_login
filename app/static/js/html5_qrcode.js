// This method will trigger user permissions
console.log("sadsaad")
function onScanSuccess(decodedText, decodedResult) {
    // Handle on success condition with the decoded text or result.
    console.log(`Scan result: ${decodedText}`, decodedResult);
}

var html5QrcodeScanner = new Html5QrcodeScanner(
    "reader", { fps: 10, qrbox: 250 },
    qrCodeMessage => {
        alert("qeewqeq")
      },
    );
  html5QrcodeScanner.render(onScanSuccess);