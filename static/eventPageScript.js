const rootUrl = "http://127.0.0.1:5000";
var currEventId = window.location.href;
currEventId = currEventId.substring(currEventId.length - 6, currEventId.length);

const addCarForm = document.getElementById("addCarForm");
const addRiderForm = document.getElementById("addRiderForm");
const copyLinkButton = document.getElementById("copyLinkButton");
copyLinkButton.setAttribute("style", "margin: 0 auto; display: block;");
// for some reason, you don't have to get the fields too, idk why

const allCarsDiv = document.createElement("div");
document.body.appendChild(allCarsDiv);
refreshCars();

copyLinkButton.addEventListener("click", async(e) => {
    navigator.clipboard.writeText(window.location.href);
    copyLinkButton.innerText = "copied link!"
    setTimeout(function() { copyLinkButton.innerText = "copy link"}, 1250);
});

addCarForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const driverName = driverNameField.value.trim();
    const numberSeats = numberSeatsField.value;
    if (!driverName) return;
    if (!numberSeats) return;

    try {
        const endpoint = rootUrl + "/api/send-car-to-mongo/" + currEventId;
        const res = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ driverName: driverName, numberSeats: numberSeats, takenSeats: 0 })
        });

        refreshCars();
    } catch (err) {
        console.log("error" + err);
    }
});

addRiderForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const riderName = riderNameField.value.trim();
    const driverName = carsDropdownField.value;
    const riderPhone = riderPhoneField.value;
    if (!riderName) return;
    if (!driverName) return;
    if (!riderPhone) return;

    try {
        const endpoint = rootUrl + "/api/send-rider-to-mongo/" + currEventId + "/" + driverName;
        const res = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ riderName: riderName, riderPhone : riderPhone })
        });

        refreshCars();
    } catch (err) {
        console.log("error" + err);
    }
});

function refreshCars() {

// clear car elements from html

allCarsDiv.innerHTML = "";

// add car elements to html

// get cars
fetch(rootUrl + "/api/get-cars-for-event/" + currEventId)
    .then((response) => response.json())
    .then((cars) => {
        for (i = 0; i < cars.length; i++) {
            let thisCar = cars[i];

            // add cars to document body, also add their riders

            let newCarDiv = document.createElement("div");
            newCarDiv.setAttribute("class", "carDiv");

            let newDriverDiv = document.createElement("div");
            newDriverDiv.setAttribute("class", "driverDiv");
            
            let newCarButton = document.createElement("button");
            newCarButton.innerText = "✖";
            newCarButton.setAttribute("class", "removeButton");
            newCarButton.addEventListener("click", async (e) => {

                try {
                    const endpoint =
                        rootUrl + "/api/remove-car-from-mongo/" + currEventId + "/" + thisCar.driverName;
                    const res = await fetch(endpoint, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ driverName: thisCar.driverName })
                    });

                    refreshCars();

                } catch (err) {
                    console.log("error" + err);
                }
            });
            newDriverDiv.appendChild(newCarButton);
            
            let newCarText = document.createElement("h3");
            newCarText.innerText =
                thisCar.driverName + ": " + thisCar.takenSeats + " / " + thisCar.numberSeats;
            newDriverDiv.appendChild(newCarText);
            
            newCarDiv.appendChild(newDriverDiv);

            // add a separator if necessary

            if (thisCar.riders.length != 0) {
                let horizontalRule = document.createElement("hr");
                horizontalRule.setAttribute("width", "100%");
                newCarDiv.appendChild(horizontalRule);
            }

            // add their riders

            let newRiderLeftDiv = document.createElement("div"); // left aligns the riders
            newRiderLeftDiv.setAttribute("class", "leftRiderDiv");

            for (j = 0; j < thisCar.riders.length; j++) {
                let newRiderDiv = document.createElement("div");
                newRiderDiv.setAttribute("class", "riderDiv");

                let thisRider = thisCar.riders[j];
                
                let newRiderButton = document.createElement("button");
                newRiderButton.innerText = "✖";
                newRiderButton.setAttribute("class", "removeButton");
                newRiderDiv.appendChild(newRiderButton);
                
                let newRiderText = document.createElement("p");
                newRiderText.innerText = thisRider.riderName + " " + makePhonePretty(thisRider.riderPhone);
                newRiderDiv.appendChild(newRiderText);               

                addClickListenerForRemoveButton(newRiderButton, thisCar.driverName, thisRider.riderName);

                newRiderLeftDiv.appendChild(newRiderDiv);
            }

            newCarDiv.appendChild(newRiderLeftDiv);

            allCarsDiv.appendChild(newCarDiv);

            // add cars to dropdown list for riders IF they have open seats
            if (thisCar.takenSeats < thisCar.numberSeats) {
                let newOption = document.createElement("option");
                newOption.text = newOption.value = cars[i].driverName;
                carsDropdownField.add(newOption, 0);
            }
        }
    });

    document.body.appendChild(allCarsDiv);

}

function addClickListenerForRemoveButton(button, driverName, riderName) {
    button.addEventListener("click", async (e) => {
        try {
            const endpoint =
                rootUrl + "/api/remove-rider-from-mongo/" + currEventId + "/" + driverName + "/" + riderName;
            const res = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: {}
            });

            refreshCars();
        } catch (err) {
            console.log("error" + err);
        }
    });
}

function makePhonePretty(phone) {
    let phoneStr = phone + "";
    return "(" + phoneStr.substring(0, 3) + ")\t" + phoneStr.substring(3, 6) + "-" + phoneStr.substring(6);
}

// Source - https://stackoverflow.com/a
// Posted by ofundefined, modified by community. See post 'Timeline' for change history
// Retrieved 2025-11-29, License - CC BY-SA 4.0

var sha256 = function sha256(ascii) {
    function rightRotate(value, amount) {
        return (value >>> amount) | (value << (32 - amount));
    }

    var mathPow = Math.pow;
    var maxWord = mathPow(2, 32);
    var lengthProperty = "length";
    var i, j; // Used as a counter across the whole file
    var result = "";

    var words = [];
    var asciiBitLength = ascii[lengthProperty] * 8;

    //* caching results is optional - remove/add slash from front of this line to toggle
    // Initial hash value: first 32 bits of the fractional parts of the square roots of the first 8 primes
    // (we actually calculate the first 64, but extra values are just ignored)
    var hash = (sha256.h = sha256.h || []);
    // Round constants: first 32 bits of the fractional parts of the cube roots of the first 64 primes
    var k = (sha256.k = sha256.k || []);
    var primeCounter = k[lengthProperty];
    /*/
    var hash = [], k = [];
    var primeCounter = 0;
    //*/

    var isComposite = {};
    for (var candidate = 2; primeCounter < 64; candidate++) {
        if (!isComposite[candidate]) {
            for (i = 0; i < 313; i += candidate) {
                isComposite[i] = candidate;
            }
            hash[primeCounter] = (mathPow(candidate, 0.5) * maxWord) | 0;
            k[primeCounter++] = (mathPow(candidate, 1 / 3) * maxWord) | 0;
        }
    }

    ascii += "\x80"; // Append Ƈ' bit (plus zero padding)
    while ((ascii[lengthProperty] % 64) - 56) ascii += "\x00"; // More zero padding
    for (i = 0; i < ascii[lengthProperty]; i++) {
        j = ascii.charCodeAt(i);
        if (j >> 8) return; // ASCII check: only accept characters in range 0-255
        words[i >> 2] |= j << (((3 - i) % 4) * 8);
    }
    words[words[lengthProperty]] = (asciiBitLength / maxWord) | 0;
    words[words[lengthProperty]] = asciiBitLength;

    // process each chunk
    for (j = 0; j < words[lengthProperty]; ) {
        var w = words.slice(j, (j += 16)); // The message is expanded into 64 words as part of the iteration
        var oldHash = hash;
        // This is now the undefinedworking hash", often labelled as variables a...g
        // (we have to truncate as well, otherwise extra entries at the end accumulate
        hash = hash.slice(0, 8);

        for (i = 0; i < 64; i++) {
            var i2 = i + j;
            // Expand the message into 64 words
            // Used below if
            var w15 = w[i - 15],
                w2 = w[i - 2];

            // Iterate
            var a = hash[0],
                e = hash[4];
            var temp1 =
                hash[7] +
                (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)) + // S1
                ((e & hash[5]) ^ (~e & hash[6])) + // ch
                k[i] +
                // Expand the message schedule if needed
                (w[i] =
                    i < 16
                        ? w[i]
                        : (w[i - 16] +
                              (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3)) + // s0
                              w[i - 7] +
                              (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10))) | // s1
                          0);
            // This is only used once, so *could* be moved below, but it only saves 4 bytes and makes things unreadble
            var temp2 =
                (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)) + // S0
                ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2])); // maj

            hash = [(temp1 + temp2) | 0].concat(hash); // We don't bother trimming off the extra ones, they're harmless as long as we're truncating when we do the slice()
            hash[4] = (hash[4] + temp1) | 0;
        }

        for (i = 0; i < 8; i++) {
            hash[i] = (hash[i] + oldHash[i]) | 0;
        }
    }

    for (i = 0; i < 8; i++) {
        for (j = 3; j + 1; j--) {
            var b = (hash[i] >> (j * 8)) & 255;
            result += (b < 16 ? 0 : "") + b.toString(16);
        }
    }
    return result;
};
