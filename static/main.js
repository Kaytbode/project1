// Launch modal to take in reviews
let focusedElementBeforeModal;

const modal = document.querySelector('.modal');
const modalOverlay = document.querySelector('.overlay');

const closeModal = ()=> {
    //hide the modal and overlay
    modal.style.display = 'none';
    modalOverlay.style.display = 'none';

    //set focus back to the element that had it before it was opened
    focusedElementBeforeModal.focus();
}

const openModal = ()=>{
    //save current focus
    focusedElementBeforeModal = document.activeElement;
    // Listen for and trap the keyboard
    modal.addEventListener('keydown', trapTabKey);
    //Listen for indicators to close the modal
    modalOverlay.addEventListener('click', closeModal);
    //close button
    //button to close modal
    const closeBtn = modal.querySelector('.close-modal');
    closeBtn.addEventListener('click', closeModal);
    //find focusable elements and convert nodelist to array
    let focusableElementsString = 'input:not([disable]), textarea:not([disabled]), button:not([disabled]), [tabindex="0"]';
    //remove hidden elements
    let focusableElements = [...modal.querySelectorAll(focusableElementsString)].filter(el=> !el.hidden);
    
    let firstTabStop = focusableElements[0],
        lastTabStop = focusableElements[focusableElements.length - 1];
    
    //show the modal and overlay
    modal.style.display = 'block';
    modalOverlay.style.display = 'block';

    //focus first child
    firstTabStop.focus();

    function trapTabKey(event) {
        //check for tab key press
        if(event.key === 'Tab'){
            //shift + tab
            if(event.shiftkey){
                if(document.activeElement === firstTabStop){
                    event.preventDefault();
                    lastTabStop.focus();
                }
            }
            //tab
            else{
                if(document.activeElement === lastTabStop){
                    event.preventDefault();
                    firstTabStop.focus();
                }
            }
        }
        //escape
        if(event.key === 'Escape'){
            closeModal(modal);
        }
    }
}

//button to launch modal
const addModal = document.querySelector('.review-button');
addModal.addEventListener('click', openModal);