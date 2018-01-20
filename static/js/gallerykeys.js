(function() {
  'use strict';

  function keyHandler(e) {
    switch (e.keyCode) {
      case 38: // <up>
      case 87: // W
        e.stopPropagation();
        e.preventDefault();
        window.scrollBy(0, -50);
        break;
      case 40: // <down>
      case 83: // S
        e.stopPropagation();
        e.preventDefault();
        window.scrollBy(0, 50);
        break;
      case 37: // <left>
      case 65: // A
        e.stopPropagation();
        e.preventDefault();
        var prev = document.querySelector('a.navbar__prev');
        if (prev !== null) {
          prev.click();
        }
        break;
      case 39: // <right>
      case 68: // D
        e.stopPropagation();
        e.preventDefault();
        document.getElementById('page__image').click();
        break;
      case 32: // <space>
        if (!e.shiftKey) {
          if ((window.innerHeight + window.scrollY) >=
              document.body.scrollHeight) {
            e.stopPropagation();
            e.preventDefault();
            document.getElementById('page__image').click();
          }
        }
        break;
    }
  }

  document.addEventListener('keydown', keyHandler);
})();
