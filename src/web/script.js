// Adding objects here will dynamically update the nav bar
const navTabs = [
    { id: 'review', label: 'Review', default: true },
    { id: 'add', label: 'Add', default: false },
    { id: 'view-cards', label: 'View Cards', default: false },
    // { id: 'explore', label: 'Explore', default: false }, // Not in use currently
    { id: 'settings', label: 'Settings', default: false }
];

// Add navigation functionality
document.addEventListener('DOMContentLoaded', function () {

    // Nav Sidebar Container
    const sidebar = document.getElementById('nav-sidebar');
    // Set of all ids mapped to nav links
    const navLinks = {};
    // Current active nav tab id, updated each time a new tab is selected
    let navIdCurr = null;
    // Create elements for each tab
    navTabs.forEach(tab => {

        // Add new list Item
        const navItem = document.createElement('li');
        navItem.className = 'nav-item';

        // Add navigation
        const navLink = document.createElement('a');
        navLink.className = `nav-link ${tab.default ? 'active' : ''}`;
        navLink.href = '#';
        navLink.id = `${tab.id}-nav`;
        navLink.textContent = tab.label;

        // Add to DOM
        navItem.appendChild(navLink);
        sidebar.appendChild(navItem);
        navLinks[tab.id] = navLink;
        const navContent = document.getElementById(`${tab.id}-content`);
        console.log(`${tab.id}-content`);

        // Make default tab active
        if (tab.default) {
            navIdCurr = tab.id;
            navContent.style.display = 'block';
        } else {
            navContent.style.display = 'none';
        }

    });

    // Add navigation functionality to each
    for (const [id, navLink] of Object.entries(navLinks)) {
        navLink.addEventListener('click', function (e) {
            e.preventDefault();
            setActiveTab(id);
        })
    }

    // Helper Function to set the selected tab to be visible and hide others
    function setActiveTab(id) {
        console.log(`id: ${id}, curr: ${navIdCurr}`);
        const activeNav = navLinks[id];
        const prevNav = navLinks[navIdCurr];
        prevNav.classList.remove('active');
        activeNav.classList.add('active');
        const prevContent = document.getElementById(`${navIdCurr}-content`);
        prevContent.style.display = 'none';
        const activeContent = document.getElementById(`${id}-content`);
        activeContent.style.display = 'block';

        navIdCurr = id;
    }

    // Show/hide answer functionality
    const showAnswerBtn = document.getElementById('show-answer');
    const answerSection = document.getElementById('answer-section');
    const ratingControls = document.getElementById('rating-controls');

    showAnswerBtn.addEventListener('click', function () {
        answerSection.classList.remove('hidden-content');
        showAnswerBtn.style.display = 'none';
        ratingControls.style.display = 'flex';
    });

});

// *** REVIEW ***
/**
 * Represents a single button used to rate an answer. Interface with the backend
 * is added via a click event listener
 */
class ratingBtn {
    constructor(id, rating) {
        this.id = id;
        this.rating = rating;
        const button = document.getElementById(this.id);
        button.addEventListener('click', function (e) {
            console.log(rating);
            eel.review_tidbit(rating)(displayReviewCard);
        });
    }
}

/** Set of buttons used to rate ease of answering */
const ratingButtons = [
    new ratingBtn("rev-again", 1),
    new ratingBtn("rev-hard", 2),
    new ratingBtn("rev-good", 3),
    new ratingBtn("rev-easy", 4)
];

/**
 * Displays the top card of the deck to review
 * 
 * @param tidbit top tidbit to display in the review section
 */
function displayReviewCard(tidbit) {

    console.log(tidbit)
    let card = document.getElementById('review-card');
    card.style = ""; // Remove any inline styling 
    let title = document.getElementById('review-title');
    if (tidbit['title'] === null) {
        title.textContent = "";
    } else {
        title.textContent = tidbit['title'];
    }

    let question = document.getElementById('review-question');
    question.textContent = tidbit['question'];
    let answer = document.getElementById('review-answer');
    answer.textContent = tidbit['data'];

    let showAnswerBtn = document.getElementById('show-answer');
    showAnswerBtn.style.display = '';
    let answerSection = document.getElementById('answer-section');
    answerSection.classList.add('hidden-content');

}

/**
 * General Function to display a card to review. This generates a card, the
 * answer is not obscured
 * 
 * @param tidbit dictionary / object with tidbit data
 * @param element DOM element to add card contents to
 */
function displayTidbit(tidbit, element) {

    console.log(tidbit)

    let card = element.appendChild(document.createElement('div'));
    card.className = 'card-body p-4';

    let title = card.appendChild(document.createElement('h5'));
    title.className = 'card-title';
    if (tidbit['title'] === null) {
        title.textContent = "";
    } else {
        title.textContent = tidbit['title'];
    }

    let question = card.appendChild(document.createElement('p'));
    question.className = 'card-text';
    question.textContent = tidbit['question'];

    let hr = card.appendChild(document.createElement('hr'));
    hr.className = 'my-3';

    let answerSection = card.appendChild(document.createElement('div'));
    answerSection.className = "answer-section";
    let answer = answerSection.appendChild(document.createElement('p'));
    answer.textContent = tidbit['data'];

    let source = card.appendChild(document.createElement('p'));
    source.className = 'text-muted';
    source.textContent = tidbit['source'];
}


// *** ADD ***
const addCreateBtn = document.getElementById('create-card-btn');
const addQuestion = document.getElementById('new-card-question');
const addDataValue = document.getElementById('new-card-content');
const addDataSource = document.getElementById('new-card-source');
const addDataTitle = document.getElementById('new-card-title');

addCreateBtn.addEventListener('click', function (e) {
    let data = addDataValue.value;
    let usrQuestion = addQuestion.value;
    let source = addDataSource.value;
    let title = addDataTitle.value;
    if (data != "") {
        eel.add_tidbit(data, usrQuestion, source, title)(displayReviewCard);
        let placeHolder = document.getElementById('review-placeholder');
        placeHolder.style = "display: none";
        eel.get_deck()(showAllCards);
        addDataValue.value = "";
        addDataSource.value = "";
        addDataTitle.value = "";
    }
})

/**
 * Displays contents of the current deck.
 */
function showAllCards(deck) {
    let cardsElement = document.getElementById('all-cards');
    cardsElement.innerHTML = '';
    deck.forEach(tid => {
        let row = cardsElement.appendChild(document.createElement('div'));
        row.className = 'row mt-3';
        let newCard = row.appendChild(document.createElement('div'));
        newCard.className = 'card h-100';
        displayTidbit(tid, newCard);
    })

}

// *** SETTINGS ***
const saveDataBtn = document.getElementById('settings-save');
const loadDataBtn = document.getElementById('settings-load');

loadDataBtn.addEventListener('click', function (e) {
    eel.load_deck()(function (hasCards) {
        if (hasCards) {
            loadDataBtn.insertAdjacentHTML(
                'afterend',
                '<div class="alert alert-success alert-dismissible" role="alert"><button type="button" class="btn-close" data-bs-dismiss="alert"aria-label="Close"></button><strong>Success!</strong>'
            );

            eel.get_deck()(function (deck) {
                let placeHolder = document.getElementById('review-placeholder');
                placeHolder.style = "display: none";
                displayReviewCard(deck[0])
                showAllCards(deck)
            });
        } else {
            loadDataBtn.insertAdjacentHTML(
                'afterend',
                '<div class="alert alert-warning alert-dismissible" role="alert"><button type="button" class="btn-close" data-bs-dismiss="alert"aria-label="Close"></button><strong>Deck is Empty</strong>'
            )
        }
    })
})

saveDataBtn.addEventListener('click', function (e) {
    eel.get_deck_size()(function (size) {
        if (size > 0) {
            eel.save_deck();
            saveDataBtn.insertAdjacentHTML(
                'afterend',
                '<div class="alert alert-success alert-dismissible" role="alert"><button type="button" class="btn-close" data-bs-dismiss="alert"aria-label="Close"></button><strong>Success!</strong>'
            )
        } else {
            saveDataBtn.insertAdjacentHTML(
                'afterend',
                '<div class="alert alert-warning alert-dismissible" role="alert"><button type="button" class="btn-close" data-bs-dismiss="alert"aria-label="Close"></button><strong>Deck is Empty</strong>'
            )
        }
    })

});
