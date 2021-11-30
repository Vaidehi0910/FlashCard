function validateCard(event){
    var cardf=document.getElementById("card_fname").value;
    var cardb=document.getElementById("card_bname").value;
    var deck=document.getElementById("deck_name").value;
    if (deck.indexOf("'")==-1 && deck.indexOf('"')==-1) {
        if (cardf.indexOf('"')==-1 && cardf.indexOf("'")==-1){
            if (cardb.indexOf('"')==-1 && cardb.indexOf("'")==-1) {
                return true
            }
            else{
                event.preventDefault()
                alert("Enter valid back of card")
                return false
            }
        }
        else{
            event.preventDefault()
            alert("Enter valid front of card")
            return false
        }
    }
    else{
        event.preventDefault()
        alert("Enter Valid Deck name")
        return false
    }
}

function validateDeck(event){
    var deck=document.getElementById("deck_name").value;
    console.log(deck)
    if (deck.indexOf('"')==-1 && deck.indexOf("'")==-1) {
        return true
    }
    else{
        event.preventDefault()
        alert("Enter Valid deck name")
        return false
    }
}

function validateForm(event){
    var user=document.getElementById("username")
    var pass=document.getElementById("password")
    if (user.indexOf('"')==-1 && deck.indexOf("'")==-1){
        if (pass.indexOf("'")==-1 && pass.indexOf('"')==-1) {
            return true
        }
        else{
            event.preventDefault()
            alert("Enter Valid Password")
            return false
        }
    }
    else{
        event.preventDefault()
        alert("Enter Valid Username")
        return false
    }
}