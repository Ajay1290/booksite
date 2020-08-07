import '../CSS/roop.css'
import '../JS/vendor/vendor.js'

$(document).ready(function(){
    
    // Loading 
    $('#loadingok').css('display','none');
    $('.main_bg').css('display','block');
    $('#all_main').css('display','block');
    $('#footer_b').css('display','block');
    
    // Hamburgur Icon Mobile
    $('#hamburger').addClass('close_ham');  
    $('#hamburger').on('click',function(){
      if ($(this)[0].classList[0] == 'close_ham'){
        $(this).addClass('open_ham');
        $(this).removeClass('close_ham');
        $('.mobile_nav').css('display','block')
        $('#contentLayer').css('display','block')
        $('body').css('overflow','hidden')
        $('.search_icon').addClass('close_s');
        $('.search_box').css('display','none')
        $('.form_search').css('width','60%')
        $('.search_icon_nav').css('top','1px')
        $('#search_box_live').css('width','85%')
        $('#search_box_live').css('margin','')
        $('.search_box').css('display','')
        $('.close_circle').addClass('open_circle')
        $('.close_bar').addClass('open_bar')
        $('.close_circle').removeClass('close_circle')
        $('.close_bar').removeClass('close_bar')
      }
      else{
        $(this).addClass('close_ham');
        $(this).removeClass('open_ham');
        $('.mobile_nav').css('display','none')
        $('#contentLayer').css('display','none')
        $('body').css('overflow','auto')
      }
    });   
  
    $("#contentLayer").on('click', function () {
      $(this).removeClass('open_ham');
      $('#hamburger').addClass('close_ham');
      $('.mobile_nav').css('display','none');
      $('#hamburger').removeClass('open_ham');
      $('#contentLayer').css('display','none');
      $('body').css('overflow','auto')
    });
  
    $('#content').on('click',function(){
        $(this).focus();
    });
  
    // Search Icon Mobile
    $('.search_icon').addClass('close_s');
    $('.search_icon').on('click',function(){
      if ($(this)[0].classList[1] == 'close_s'){
        $(this).removeClass('close_s');
        $(this).addClass('open_s');
        $('.form_search').css('width','100%')
        $('.search_icon_nav').css('top','11px')
        $('#search_box_live').css('width','100%')
        $('#search_box_live').css('margin','10px 0 0 0')
        $('.search_box').css('display','block')
        $('.mobile_nav').css('display','none');
        $('#hamburger').addClass('close_ham');
        $('#hamburger').removeClass('open_ham');
        $('body').css('overflow','auto')
        $('.open_circle').addClass('close_circle')
        $('.open_bar').addClass('close_bar')
        $('.open_circle').removeClass('open_circle')
        $('.open_bar').removeClass('open_bar')
        $('#search_box_live').focus();
      }else{
        $(this).removeClass('open_s');
        $(this).addClass('close_s');
        $('.search_box').css('display','none')
        $('.form_search').css('width','60%')
        $('.search_icon_nav').css('top','1px')
        $('#search_box_live').css('width','85%')
        $('#search_box_live').css('margin','')
        $('.search_box').css('display','')
        $('body').css('overflow','auto')
        $('.close_circle').addClass('open_circle')
        $('.close_bar').addClass('open_bar')
        $('.close_circle').removeClass('close_circle')
        $('.close_bar').removeClass('close_bar')
      }
    });
  
    $(window).on('resize', function() {
      if ($(this).width() <= 1000) {
        $('#main_larg').removeClass('col-md-9');
        $('#open_nav').addClass('openlet');
        // Navbar Tricks
        var prevScrollpos = window.pageYOffset;
        window.onscroll = function() {
          var currentScrollPos = window.pageYOffset;
          if (prevScrollpos > currentScrollPos) {
            $(".openlet").css('top','0px')
          } else {
            $(".openlet").css('top','-50px')
          }
          prevScrollpos = currentScrollPos;
        } 
      }
      if ($(this).width() > 1000) {
        $('#main_larg').addClass('col-md-9');
        $('#open_nav').removeClass('openlet');
        $('#open_nav').css('top','0px');
      }
      if ($(this).width() <= 530) {
        $('.mai_row').addClass('row mai_row');
        $('.okp').removeClass('media');
      }
      if ($(this).width() > 530) {
        $('.mai_row').removeClass('row');
        $('.okp').addClass('media');
        $('.sid_i').removeClass('col-3');
        $('.im_co').addClass('img-thumbnail');
        $('.sid_i').removeClass('im_co_wrap mr-3');
      }
    });
  
    if ($(window).width() < 530) {
      $('.mai_row').addClass('row mai_row');
      $('.okp').removeClass('media');
    }
    if ($(window).width() > 530) {
      $('.mai_row').removeClass('row');
      $('.okp').addClass('media');
      $('.sid_i').removeClass('col-3');
      $('.im_co').addClass('img-thumbnail');
      $('.sid_i').removeClass('im_co_wrap mr-3');
    }
    if ($(window).width() <= 1000) {
      $('#main_larg').removeClass('col-md-9');
      $('#open_nav').addClass('openlet');
        // Navbar Tricks
        var prevScrollpos = window.pageYOffset;
        window.onscroll = function() {
          var currentScrollPos = window.pageYOffset;
          if (prevScrollpos > currentScrollPos) {
            $(".openlet").css('top','0px')
          } else {
            $(".openlet").css('top','-50px')
          }
          prevScrollpos = currentScrollPos;
        } 
    }
    if ($(window).width() > 1000) {
      $('#open_nav').removeClass('openlet');
      $('#open_nav').css('top','0px');
    }
  });
  document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll('[data-src]')
    function preloadImage(img){
      const src = img.getAttribute('data-src');
      if(!src){
        return;
      }
      img.src = src;
    }
    const imgOptions = {
      threshold : 0.7,
      rootMargin: '0px 0px 100px 0px'
    };
    const imgObserver = new IntersectionObserver((entries,imageObserver) =>{
      entries.forEach(entry => {
        if(!entry.isIntersecting){
          return;
        }else{
          preloadImage(entry.target);
          imageObserver.unobserve(entry.target);
          entry.target.removeAttribute('data-src');
          entry.target.removeAttribute('data-srcset');
        }
      });
    }, imgOptions);
  
    images.forEach(image =>{
      imgObserver.observe(image);
    });
  });
  