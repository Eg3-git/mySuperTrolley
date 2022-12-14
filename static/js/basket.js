var basketButtons = document.getElementsByClassName('update-basket')
console.log(basketButtons)

for (var i=0; i<basketButtons.length; i++) {
    basketButtons[i].addEventListener('click', function () {
        var pID = this.dataset.product
        var action = this.dataset.action
        console.log('ID: ', pID, 'Action: ', action)
        console.log('USER:', user)
        if (user === 'AnonymousUser') {
            console.log("not Authenticated")
        } else {
            updateUserOrder(pID, action)
        }
    })
}

function updateUserOrder(pID, action){
    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,},
        body:JSON.stringify({'productID':pID, 'action':action})
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('Data', data)
            location.reload()
        })
}