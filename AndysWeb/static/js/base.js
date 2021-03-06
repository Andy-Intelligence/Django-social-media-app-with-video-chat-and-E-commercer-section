document.addEventListener('DOMContentLoaded',()=>{
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    if ($navbarBurgers.Length > 0){
        $navbarBurgers.array.forEach(el => {
            el.addEventListener('click', ()=> {
                const target = el.dataset.target;
                const $target = document.getElementById(target);

                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');
            });
            
        });
    }
});