// poptrox popup

$(window).on('load', function () {
  const foo = $('.pop-gallery');
  foo.poptrox({
    baseZIndex: 20000,
    fadeSpeed: 300,
    overlayOpacity: 0,
    popupCloserText: '',
    popupLoaderText: '&bull;&bull;&bull;&bull;',
    popupSpeed: 300,
    popupWidth: 150,
    popupHeight: 150,
    usePopupCaption: true,
    popupBlankCaptionText: '',
    popupLoaderSelector: '.loader',
    popupLoaderTextSize: '2em',
    usePopupCloser: false,
    usePopupDefaultStyling: true,
    usePopupForceClose: true,
    usePopupLoader: true,
    usePopupNav: true,
    windowMargin: 20
  });
});