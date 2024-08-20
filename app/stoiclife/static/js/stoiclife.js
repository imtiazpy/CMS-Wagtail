const backToTopBtn = document.getElementById('back-to-top-btn');

// Hide the button initially
backToTopBtn.style.display = 'none';

// scroll threshold
const scrollThreshold = 400; 

// Function to scroll to the top of the page
function scrollToTop() {
  window.scrollTo({
      top: 0,
      behavior: 'smooth' // Smooth scrolling behavior
  });
}

// scroll event listener to the window
window.addEventListener('scroll', () => {
  // current scroll position
  const scrollY = window.scrollY;

  // If the scroll position is beyond the threshold, show the button
  if (scrollY > scrollThreshold) {
    backToTopBtn.style.display = 'block';
  } else {
    // Otherwise, hide the button
    backToTopBtn.style.display = 'none';
  }
});

// click event listener to the back-to-top button
backToTopBtn.addEventListener('click', scrollToTop);


// used for onclick event of card element (Slide up, News )
function redirectToPage(card) {
  const pageUrl = card.getAttribute('data-page');
  const open_in_new = card.getAttribute('data-open');
  if (open_in_new == 'True') {
    window.open(pageUrl, '_blank');
  } else {
    window.location.href = pageUrl;
  }
}


// Open external links on another tab
$(document).ready(function(){
  $('a[href^="http"]').attr({'target': '_blank', 'rel': 'nofollow noopener'});
});