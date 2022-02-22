const navSlide = ()=> {
    const burger = document.querySelector('.burger');
    // const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');
    
    const nav = document.getElementsByTagName('ul')[0];
    burger.addEventListener('click', ()=> {
        // Toggle Nav
        nav.classList.toggle('nav-active');
        nav.classList.add('transition');
        //Animate links
        navLinks.forEach((link,index) => {
            if(link.style.animation){
                link.style.animation = ``
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.5}s`
            }        
        
        });
        
        burger.classList.toggle('toggle');
    });
}


const componentDidMount = ()=> {
    const nav = document.getElementsByTagName('ul')[0];
    window.addEventListener(
      'resize',
      () => {
        if (window.innerWidth > 1035) {
          nav.classList.remove('transition');
        }
      },
      false
    );
  }

navSlide();
componentDidMount()