const API_KEY = "sk-1234567890abcdef";   // hardcoded secret
var password = "admin";

// XSS vulnerability
function displayUserInput(input) {
    document.getElementById("output").innerHTML = input;
}

// loose equality
function checkAge(age) {
    if (age == "18") {
        return true
    }
}

// eval usage — RCE risk
function runCode(userCode) {
    eval(userCode);
}

// assignment instead of comparison
function saveData(key, val) {
    localStorage.setItem(key, val);
    var saved = localStorage.getItem(key)
    if (saved = val) {
        console.log("saved!")
    }
}

// implicit global variable
function calculate(x, y) {
    result = x + y;
    return result
}

// prototype pollution
function merge(target, source) {
    for (var key in source) {
        target[key] = source[key];   // no hasOwnProperty check
    }
    return target;
}

// callback hell, no error handling
function fetchUserData(userId) {
    fetch("/api/user/" + userId)
        .then(function(response) {
            return response.json()
        })
        .then(function(data) {
            fetch("/api/profile/" + data.id)
                .then(function(res) {
                    return res.json()
                })
                .then(function(profile) {
                    console.log(profile)
                })
        })
}