function makeRequest(method, url, body) {
    return new Promise(
        function (resolve, reject) {
            let req = new XMLHttpRequest();

            req.onload = function () {
                const data = JSON.parse(req.responseText);
                if (req.status >= 200 && req.status < 300) {
                    resolve(data);
                } else {
                    const reason = new Error('Rejected');
                    reject(reason);
                }
            };

            req.open(method, url);
            req.send(JSON.stringify(body));
        }
    );
}


function createAccount() {
    let newAcc = {
        "firstName": document.getElementById("firstName").value,
        "lastName": document.getElementById("lastName").value
    };
    makeRequest("POST", "/server/addAccount", newAcc)
        .then((data) => {
	console.log(data);
        })
        .catch((error) => console.log(error.message));
    return false;
}
