// Made by github.com/zebbern

// Define the target username and URL
const targetUsername = "@test";
const targetURL = "https://link.com";

// Function to input the URL into the search field
function inputURL(callback) {
    const urlInput = document.querySelector("body > div.col-sm-5.col-xs-12.p-1.container.t-chearts-menu > div > form > div > input");
    if (urlInput) {
        urlInput.value = targetURL; // Input the target URL
        const event = new Event("input"); // Trigger the input event
        urlInput.dispatchEvent(event);
        console.log(`URL "${targetURL}" inputted successfully!`);
        setTimeout(callback, 1000); // Wait 1 second before moving to the next step
    } else {
        console.log("URL input field not found.");
    }
}

// Function to click the search button
function clickSearchButton(callback) {
    const searchButton = document.querySelector('form[action="c2VuZC9mb2xsb3dlcnNfdGlrdG9r"] button[type="submit"]');
    if (searchButton) {
        searchButton.click();
        console.log("Search button clicked successfully!");
        setTimeout(callback, 2000); // Wait 2 seconds for the page to load
    } else {
        console.log("Search button not found.");
    }
}

// Function to click `.wbutton`
function clickWButton(callback) {
    const wButton = document.querySelector('.wbutton');
    if (wButton) {
        wButton.click();
        console.log(".wbutton clicked successfully!");
        setTimeout(callback, 2000); // Wait 2 seconds for the page to load
    } else {
        console.log(".wbutton not found.");
    }
}

// Function to search for the username and click the button
function searchAndClickButton() {
    // Find the div containing the target username
    const userDiv = Array.from(document.querySelectorAll('.font-weight-bold.d-inline-flex.kadi-rengi'))
        .find(div => div.textContent.trim() === targetUsername);

    if (userDiv) {
        console.log(`Found the username: ${targetUsername}`);

        // Navigate to the parent form
        const form = userDiv.closest('form');

        if (form) {
            // Find the button inside the form
            const button = form.querySelector('button.btn.btn-primary.rounded-0');

            if (button) {
                // Click the button
                button.click();
                console.log(`Button clicked for username: ${targetUsername}`);
            } else {
                console.log("Button not found in the form.");
            }
        } else {
            console.log("Form not found for the username.");
        }

        // Update dropdowns globally
        updateDropdownsInForm();

        return true; // Username found
    } else {
        console.log(`Username ${targetUsername} not found on this page.`);
        return false; // Username not found
    }
}

// Function to update dropdowns globally
function updateDropdownsInForm() {
    const selectDropdowns = document.querySelectorAll('select[name="select_lmt"].form-select.dark-select.text-dark.rounded-0.font-weight-bold.mb-1.mt-1.p-1');

    // Loop through each dropdown and set its value to 100
    selectDropdowns.forEach(dropdown => {
        if (dropdown) {
            dropdown.value = "100";

            // Trigger the change event in case the page needs it to register the change
            const event = new Event("change");
            dropdown.dispatchEvent(event);

            console.log("Dropdown value set to 100 successfully for one element!");
        }
    });

    console.log(`Updated ${selectDropdowns.length} dropdown(s) to 100.`);
}

// Function to click the "Next" button
function clickNextButton(callback) {
    const nextButton = document.querySelector('li.page-item form button[type="submit"].btn.btn-light.rounded-0.font-weight-bold');

    if (nextButton) {
        nextButton.click();
        console.log("Next button clicked. Waiting for the next page to load...");
        setTimeout(callback, 3000); // Wait 3 seconds for the next page to load
        return true;
    } else {
        console.log("Next button not found. Reached the end of pages.");
        return false;
    }
}

// Main function to search for the username and navigate pages if not found
function searchUntilFound() {
    // Always update dropdowns at the start of each cycle
    updateDropdownsInForm();

    const found = searchAndClickButton();

    if (!found) {
        const nextExists = clickNextButton(searchUntilFound);

        if (!nextExists) {
            console.log("No more pages to search. Username not found.");
        }
    }
}

// Function to run the full process
function runWorkflow() {
    console.log("Starting workflow...");
    inputURL(() => {
        clickSearchButton(() => {
            clickWButton(() => {
                searchUntilFound();
            });
        });
    });

    // Schedule the next run in 70 seconds
    setTimeout(runWorkflow, 70000); // 70 seconds = 70000 ms
}

// Start the process
runWorkflow();


// Made by github.com/zebbern
