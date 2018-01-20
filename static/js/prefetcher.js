(function() {
  'use strict';

  function GET(url, onSuccess, onError) {
    var xhr = new XMLHttpRequest();
    xhr.onload = onSuccess;
    xhr.onerror = onError;
    xhr.open('GET', url);
    xhr.send();
  }

  function prefetch() {
    var galleryLink = document.querySelector('#gallery__link>a').href;
    var segments = galleryLink.split('/');
    var galleryId = parseInt(segments[segments.length - 1], 10);
    var page = parseInt(document.querySelector('.navbar__current').textContent);
    var url = '/gallery/' + galleryId + '/' + page + '/prefetch';
    GET(url, function() {console.log('Yey')}, function() {console.log('Ney')});
  }

  prefetch();
})();
