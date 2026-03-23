// script.js
const navLinks = document.querySelectorAll('nav a');

navLinks.forEach((link) => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        document.querySelector(`${link.href}Element`).scrollIntoView({ behavior: 'smooth' });
    });
});

const skillsList = document.querySelector('#skills ul');
const skillItems = skillsList.children;

skillItems.forEach((skill) => {
    skill.addEventListener('mouseover', () => {
        skill.style.backgroundColor = '#ccc';
    });
    skill.addEventListener('mouseout', () => {
        skill.style.backgroundColor = '#f5f5f5';
    });
});

const contactForm = document.querySelector('#contact');
const contactText = document.querySelector('#contact p');

contactForm.addEventListener('mouseover', () => {
    contactText.innerText = 'Feel free to contact me at your convenience!';
});

contactForm.addEventListener('mouseout', () => {
    contactText.innerText = 'Contact me at your convenience!';
});