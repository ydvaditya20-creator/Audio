const startBtn =
document.getElementById("startBtn");

const audioBtn =
document.getElementById("audioBtn");

const videoBtn =
document.getElementById("videoBtn");

const downloadBtn =
document.getElementById("downloadBtn");

const questionsDiv =
document.getElementById("questions");

const audioPlayer =
document.getElementById("audio");

const canvas =
document.getElementById("canvas");

const ctx =
canvas.getContext("2d");

let questions = [];

let audioBlob = null;

let finalVideo = null;

startBtn.onclick =
async ()=>{

let amount =
prompt(
"Number of Questions?"
);

if(!amount)return;

let url =
`https://opentdb.com/api.php?amount=${amount}`;

let response =
await fetch(url);

let data =
await response.json();

questions =
data.results;

showQuestions();

};

function decodeHtml(html){

let txt =
document.createElement(
"textarea"
);

txt.innerHTML = html;

return txt.value;

}

function showQuestions(){

questionsDiv.innerHTML = "";

questions.forEach(
(q,index)=>{

let area =
document.createElement(
"textarea"
);

area.id =
"q"+index;

area.value =
decodeHtml(
q.question
);

questionsDiv.appendChild(
area
);

});

}

audioBtn.onclick =
async ()=>{

let text = "";

questions.forEach(
(q,index)=>{

text +=
"Question "
+(index+1)
+". ";

text +=
document
.getElementById(
"q"+index
)
.value;

text += ". ";

});

const response =
await fetch(
"https://YOUR-APP.onrender.com/tts",
{
method:"POST",
headers:{
"Content-Type":
"application/json"
},
body:JSON.stringify({
text
})
}
);

const json =
await response.json();

const bytes =
Uint8Array.from(
atob(json.audio),
c=>c.charCodeAt(0)
);

audioBlob =
new Blob(
[bytes],
{
type:"audio/mp3"
}
);

audioPlayer.src =
URL.createObjectURL(
audioBlob
);

alert(
"Audio Ready"
);

};

function wrapText(
ctx,
text,
x,
y,
maxWidth,
lineHeight
){

const words =
text.split(" ");

let line = "";

for(
let n=0;
n<words.length;
n++
){

let testLine =
line +
words[n] +
" ";

let metrics =
ctx.measureText(
testLine
);

if(
metrics.width >
maxWidth
&& n>0
){

ctx.fillText(
line,
x,
y
);

line =
words[n]+" ";

y += lineHeight;

}
else{

line =
testLine;

}

}

ctx.fillText(
line,
x,
y
);

}

function drawQuestion(
text
){

ctx.fillStyle =
"white";

ctx.fillRect(
0,
0,
canvas.width,
canvas.height
);

ctx.fillStyle =
"black";

ctx.font =
"60px Arial";

wrapText(
ctx,
text,
80,
200,
1100,
80
);

}
