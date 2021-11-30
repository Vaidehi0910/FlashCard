const card=document.getElementById("card")
const sco=card.dataset.score
const value=card.dataset.card
const json = value;
const obj = JSON.parse(json);
const scor=JSON.parse(sco);
var showanswer=document.getElementById("b-ans")
var easybutton=document.getElementById("easy")
var medbutton=document.getElementById("medium")
var hardbutton=document.getElementById("hard")
var butt=document.getElementById("buttons")
var score=0
var ecount=0
var mcount=0
var dcount=0
var tcount=0
var avgs=0
var i=0

window.onload=showFirst()



// onload window show 1st card
function showFirst(){
    c1=Object.keys(obj)[i];
    var tag= document.createElement("p");
    tag.setAttribute("id","text")
    var ele=document.getElementById("new");
    if (c1==undefined){
        var text=document.createTextNode("No Card in Deck")
        removeallButtons();
        removeProperties();
    }
    else{
    var text = document.createTextNode(c1);
    i=i+1;
    card_score()
    }
    tag.appendChild(text);
    ele.appendChild(tag);
    removedifButtons();
}

// show card score
function card_score(){
    var p=document.getElementById("card_score");
    if (p.hasChildNodes()){
        p.removeChild(p.childNodes[0]);
    }
    var sc=Object.values(scor)[i-1];
    var tex=document.createTextNode(sc);
    p.append(tex);
}

// remove deck-card properties
function removeProperties(){
    var p=document.getElementById("remove")
    var d=document.getElementById("properties")
    p.removeChild(d)
}

// add show ans button
function addshowansButt(){
    butt.appendChild(showanswer);
}

// add difficulty buttons
function adddiffButt(){
    
    butt.appendChild(easybutton);
    butt.appendChild(medbutton);
    butt.appendChild(hardbutton);
}

// remove show ans button
function removeansButton(){
    butt.removeChild(showanswer);
}

// remove difficulty button
function removedifButtons(){
    butt.removeChild(easybutton);
    butt.removeChild(medbutton);
    butt.removeChild(hardbutton);
}

// remove all buttons 
function removeallButtons(){
    removeansButton();
    removedifButtons();
}

// show next card and calculate the score
function nextCard(id){
    var x=document.getElementById("new")
    var t=document.getElementById("text")
    x.removeChild(t);
    var a= document.getElementById("ans");
    var b=document.getElementById("ans-1");
    a.removeChild(b);

    removedifButtons();
    addshowansButt();

    if(id=='easy'){
        score=score+10;
        ecount+=1;
        sendCardScore(id,Object.keys(obj)[i-1],Object.values(obj)[i-1]);
    }
    if(id=='medium'){
        score=score+5;
        mcount+=1;
        sendCardScore(id,Object.keys(obj)[i-1],Object.values(obj)[i-1]);
    }
    if(id=='hard'){
        score=score+2;
        dcount+=1;
        sendCardScore(id,Object.keys(obj)[i-1],Object.values(obj)[i-1]);
    }
    tcount=ecount+mcount+dcount;
    avgs=score/tcount;

    var c=Object.keys(obj)[i];
    var tag1=document.createElement("p");
    tag1.setAttribute("id","text");

    if (c==undefined){
        var text=document.createTextNode("Deck is finished");
        removeansButton()
        sendScore(avgs);
        removeProperties();
    }
    else{
        var text=document.createTextNode(c);
        i+=1;
        card_score()
}
    tag1.appendChild(text);
    x.appendChild(tag1);
}

// show back side of card
function showans(){
    removeansButton();
    adddiffButt();
    var a=Object.values(obj)[i-1];
    var tag2= document.createElement('p');
    tag2.setAttribute('id','ans-1');
    var ans=document.createTextNode(a);
    tag2.appendChild(ans);
    var y=document.getElementById("ans");
    y.appendChild(tag2);
}

// sending score to flask application through http
function sendScore(avgs){
    let score={
        'score':avgs,
    }
    const request= new XMLHttpRequest();
    request.open('POST',`/score/${JSON.stringify(score)}`);
    request.onload=() => {
        const flaskMessage= request.responseText
        console.log(flaskMessage)
    }
    request.send();
}

function sendCardScore(id,cardf,cardb){
    let cscore={
        'difficulty': id,
        'card_front': cardf,
        'card_back' : cardb,
    }
    const request= new XMLHttpRequest();
    request.open('POST',`/cardscore/${JSON.stringify(cscore)}`);
    request.onload=() => {
        const flaskMessage= request.responseText
        console.log(flaskMessage)
    }
    request.send();
}

