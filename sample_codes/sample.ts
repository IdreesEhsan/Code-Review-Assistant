// hardcoded token
const AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.secret";

// any kills type safety everywhere
function processData(data: any): any {
    return data.value.nested.field;   // runtime crash if nested is undefined
}

// no input validation, XSS risk
function renderHtml(userInput: string): void {
    document.body.innerHTML = userInput;
}

// missing return type, logic error
function calculateDiscount(price, discount) {
    if (discount > 1) {
        return price - discount;   // should be price * (1 - discount)
    }
    // missing else — returns undefined
}

// async with no error handling
async function fetchOrders(userId: string) {
    const response = await fetch(`/api/orders/${userId}`);
    const data = await response.json();   // no status check
    return data;
}

// type assertion abuse — bypasses checks
function getUser(id: string) {
    return {} as User;   // dangerous cast, pretends empty object is a User
}

// memory leak — event listener never removed
function attachHandler(element: HTMLElement) {
    element.addEventListener("click", () => {
        console.log("clicked");
    });
    // listener never removed even when element is destroyed
}

// sensitive data in localStorage
function cacheUserCredentials(username: string, password: string) {
    localStorage.setItem("username", username);
    localStorage.setItem("password", password);   // never store passwords client-side!
}