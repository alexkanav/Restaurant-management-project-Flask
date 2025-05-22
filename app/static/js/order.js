const addition = {};


function choiceOfTable(tableNumber) {
    updateClasses('.popup__bg, .popup', ['active']);
    sessionStorage.setItem('table_number', tableNumber);
    orderProcessing();
}


function choiceOfDish(val, dishCode) {
    sessionStorage.setItem(dishCode, val);
    choiceOfDishAdd(dishCode);
    const greetingEl = [
        document.getElementById(dishCode),
        document.getElementById(`${dishCode}pop`),
        document.getElementById(`${dishCode}rec`)
    ];

    for (let el of greetingEl) {
        if (el) {
            el.style.backgroundColor = "#86786b";
            el.style.color = "#fff2f1";
            el.value = val;
        };
    };
}


function choiceOfDishAdd(dishCode) {
    // updateClasses(selector, classListToAdd = [], classListToRemove = [])
    updateClasses(`.add_ch_${dishCode}`, ['add-bg-col']);
}


function addAddition(id, code, description) {
    const existAdd = sessionStorage.getItem(code);
    if (existAdd) {
        if (!addition[code]) {
            addition[code] = [];
        }
        const obj = menuAdd[code];
        Object.keys(obj).forEach(key => {
            if (id.startsWith(key)) {
            addition[code].push(key);
            updateClasses(`[id^="${key}"]`, ['badd'], ['add-bg-col']);
            }
        });
    } else {
        window.alert(`Спочатку замовляється - ${description}`);
    }
}


function orderForm(obj) {
    let incDish = '';
    let orderSum = 0;

    for (const [name, value] of Object.entries(obj)) {
        if (name === 'table_number') {
            document.getElementById('display_table_number').textContent = value;

        } else  if (menuAdd.hasOwnProperty(name - 1)) {
            let additionText  = '';
            value.forEach(item => {
                orderSum += menuAdd[name - 1][item] || 0;
                additionText += `${menuAddUa[name - 1][item]}, `;
            });
            incDish +=  `<span style="font-size:12px"> --------- Додатки : ${additionText } <br /></span>`;
        } else {
        const dishName = dishAttributes[name]?.[0] || name;
            incDish += `${dishName} - в кількості  ${value} <br />`;
            orderSum += value * (price[name] || 0);
        };
    }

    return [incDish, orderSum]
}


function orderProcessing()  {

    // Save additions to sessionStorage
    writeToSessionStorage (addition);

    const completeOrder = getFromSessionStorage();
    if (!completeOrder) {
        console.error('No order data found.');
        return;
    }

    const [orderHTML, orderSum] = orderForm(completeOrder);

    document.getElementById('display_dish').innerHTML = orderHTML;
    document.getElementById('final_sum').textContent  = orderSum;

    sessionStorage.setItem('sum', orderSum);

}


function showOrder() {
    // updateClasses(selector, classListToAdd = [], classListToRemove = [])
    updateClasses('.block-table', ['block']);
    updateClasses('.block-choice-dish, .footer', ['hidden']);
}

async function sendOrder() {
    const order = getFromSessionStorage();

    if (!order) {
        window.location.replace("/faulty");
        return;
    }

    try {
        await sendToServer(order, "/post-order");
        sessionStorage.clear();
        window.location.replace("/upload-comment");
    } catch (error) {
        window.location.replace("/faulty");
    }
}


const cancelBtn = document.getElementById('cancel_order');
if (cancelBtn) cancelBtn.addEventListener('click', cancelOrder);

const confirmBtn = document.getElementById('confirm_order');
if (confirmBtn) confirmBtn.addEventListener('click', sendOrder);

const addBtn = document.getElementById('add_order');
if (addBtn) addBtn.addEventListener('click', showOrder);


document.querySelectorAll('.table-btn').forEach(button => {
    button.addEventListener('click', () => {
        const tableNumber = button.dataset.table;
        choiceOfTable(tableNumber);
    });
});

document.querySelectorAll('.amount').forEach(select => {
    select.addEventListener('change', event => {
        const code = select.dataset.code;
        const value = select.value;
        choiceOfDish(value, code);
    });
});