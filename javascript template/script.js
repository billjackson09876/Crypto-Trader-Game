'use strict';

const modalBuy = document.querySelector('.modal-buy');
const modalSell = document.querySelector('.modal-sell');
const overlay = document.querySelector('.overlay');
const btnCloseModal = document.querySelectorAll('.close-modal');
const btnOpenModalBuy = document.querySelector('.show-modal-buy');
const btnOpenModalSell = document.querySelector('.show-modal-sell');

const closeModal = function () {
  modalBuy.classList.add('hidden');
  modalSell.classList.add('hidden');
  overlay.classList.add('hidden');
};

const openModalBuy = function () {
  modalBuy.classList.remove('hidden');
  overlay.classList.remove('hidden');
};

const openModalSell = function () {
  modalSell.classList.remove('hidden');
  overlay.classList.remove('hidden');
};

for (let i = 0; i < btnCloseModal.length; i++) {
  btnCloseModal[i].addEventListener('click', closeModal);
}

btnOpenModalBuy.addEventListener('click', openModalBuy);
btnOpenModalSell.addEventListener('click', openModalSell);
overlay.addEventListener('click', closeModal);
