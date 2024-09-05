document.getElementById('generateBtn').addEventListener('click', async () => {
    // Get the values from the input fields
    const inputText = document.getElementById('inputText').value;
    const noQues = document.getElementById('noQues').value;
    const difficulty = document.getElementById('difficulty').value;

    // Make a POST request to the '/generate' endpoint with the input data
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input_text: inputText, no_ques: noQues, difficulty: difficulty }),
    });

    // Parse the JSON response
    const data = await response.json();

    // Select the element where you want to display the quiz
    const quizContainer = document.getElementById('quizContainer');
    quizContainer.innerHTML = ''; // Clear any previous content

    //hERE I will be contacting though and among us
    // Loop through the returned questions and options
    data.forEach((item, index) => {
        // Create a new div for each question
        const questionDiv = document.createElement('div');
        questionDiv.classList.add('question');

        // Create and append the question text
        const questionText = document.createElement('p');
        questionText.textContent = `${index + 1}. ${item.question}`;
        questionDiv.appendChild(questionText);

        // Create a form for the options
        const optionsForm = document.createElement('form');
        optionsForm.classList.add('options-form');
        
        // Loop through each option and add it as a radio button
        item.options.forEach((option, i) => {
            const optionLabel = document.createElement('label');
            optionLabel.classList.add('option-label');
            
            const optionInput = document.createElement('input');
            optionInput.type = 'radio';
            optionInput.name = `question-${index}`;
            optionInput.value = option;
            optionInput.id = `question-${index}-option-${i}`;

            const optionText = document.createElement('span');
            optionText.textContent = option;

            // Append radio button and text to label
            optionLabel.appendChild(optionInput);
            optionLabel.appendChild(optionText);

            // Append label to form
            optionsForm.appendChild(optionLabel);
        });

        // Append the form to the question div
        questionDiv.appendChild(optionsForm);
        // Append the question div to the quiz container
        quizContainer.appendChild(questionDiv);
        console.log(item.answer)
    });
});
