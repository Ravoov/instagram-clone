let index = 0;

const video = document.getElementById("videoplayer");
const source = document.getElementById("videosource");

let question_text = "What is the top comment?";


window.onload = () => {
    nextVideo();
};

document.getElementById("playButton").addEventListener("click", () => {
    nextVideo();
});


function nextVideo() {
    fetch(`http://localhost:8080/video?index=${index}`)
        .then((response) => response.json())
        .then((data) => {
            console.log("video received");
            console.log(data);

            index++;

            // Load video
            source.src = data.video;
            video.load();
            video.play();

            // Normalize correct answer letter
            const correct_answer = data.correct_answer.trim().toLowerCase();

            console.log("Choices:", data.choice_a, data.choice_b, data.choice_c, data.choice_d);
            console.log("Correct:", correct_answer);

            // Render question
            renderKahootMCQ(
                question_text,
                data.choice_a,
                data.choice_b,
                data.choice_c,
                data.choice_d,
                correct_answer
            );
        })
        .catch((error) => {
            console.error("Failed to fetch video:", error);
        });
}


function renderKahootMCQ(questionText, choice_a, choice_b, choice_c, choice_d, correctLetter) {
    const q = document.getElementById("question");
    const a = document.getElementById("answers");

    q.innerText = questionText;
    a.innerHTML = "";

    const choices = [
        { text: choice_a, letter: "a" },
        { text: choice_b, letter: "b" },
        { text: choice_c, letter: "c" },
        { text: choice_d, letter: "d" }
    ];

    const colors = ["kahoot-red", "kahoot-blue", "kahoot-yellow", "kahoot-green"];

    choices.forEach((choiceObj, i) => {
        const btn = document.createElement("button");
        btn.className = `kahoot-btn ${colors[i]}`;
        btn.innerText = choiceObj.text;

        btn.onclick = () => {
            const isCorrect = choiceObj.letter === correctLetter;

            if (isCorrect) {
                btn.style.background = "#4CAF50";
                alert("Correct!");
            } else {
                btn.style.background = "#B00020";
                alert("Wrong!");
            }

            nextVideo();
        };

        a.appendChild(btn);
    });
}