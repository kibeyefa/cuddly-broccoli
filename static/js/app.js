const chat_list = document.querySelector('.chat-list');
const search_bar = document.getElementById('search');
const chats = document.querySelectorAll('.chat-link');
const closeSearch = document.getElementById('close-search');
const search = document.getElementById('search');
const searchIcon = document.getElementById('search-icon');
const chatHeading = document.getElementById('chats');

search_bar.addEventListener('input', (e) => {
  let query = e.target.value.toLowerCase();

  chats.forEach((chat) => {
    let chat_name =
      chat.firstElementChild.children[1].firstElementChild.innerText.toLowerCase();
    if (chat_name.includes(query)) {
      chat.classList.remove('d-none');
    } else {
      chat.classList.add('d-none');
    }
  });
});

searchIcon.addEventListener('click', () => {
  searchIcon.classList.add('d-none');
  chatHeading.classList.add('d-none');
  search.classList.remove('d-none');
  closeSearch.classList.remove('d-none');
});

closeSearch.addEventListener('click', () => {
  searchIcon.classList.remove('d-none');
  chatHeading.classList.remove('d-none');
  search.classList.add('d-none');
  closeSearch.classList.add('d-none');

  chats.forEach((chat) => {
    chat.classList.remove('d-none');
  });
});
const form = document.getElementById('form');

const updateChatList = async function (msg_id) {
  const me = document.getElementById('me').innerText;
  const chat_list = document.querySelector('.chat-list');
  let res = await fetch(`/chat/api/${me}`);
  let data = await res.json();
  console.log(data);
  chat_list.innerHTML = '';

  data.forEach((chat, index) => {
    console.log(chat);
    let a = document.createElement('a');
    a.setAttribute('id', chat.chat_id);
    a.classList.add('chat-link');
    if (chat.type === 'personal') {
      a.setAttribute('href', `/chat/${chat.username}`);
      a.innerHTML = `
        <div class="d-flex chat text-black align-items-center px-3 ${
          index == 0 && 'first-thread'
        } ${
        chat.chat_id == msg_id &&
        window.location.pathname != '/chat/' &&
        'active'
      }">
        <div>
            <img src=${chat.image_url} class=" rounded-circle" width="45px" />
        </div>

        <div class="flex-fill ms-2">
            <h6 class="mb-0">
              ${chat.first_name} ${chat.last_name}
            </h6>
            <p class="small text-truncate mb-0 pb-0" title="${
              chat.last_message
            }">
              ${chat.last_message}
            </p>
        </div>
      </div>
    `;
    } else {
      a.setAttribute('href', `/chat/groups/${chat.i_d}`);
      a.innerHTML = `
        <div class="d-flex chat text-black align-items-center px-3 ${
          index == 0 && 'first-thread'
        } ${
        chat.chat_id == msg_id &&
        window.location.pathname != '/chat/' &&
        'active'
      }">
          <div>
              <img src=${chat.image_url} class=" rounded-circle" width="45px" />
          </div>

          <div class="flex-fill ms-2">
              <h6 class="mb-0">${chat.name}</h6>
              <p class="small text-truncate mb-0 pb-0" title="${
                chat.last_message == null ? '' : chat.last_message
              }">
                ${chat.last_message == null ? '' : chat.last_message}
              </p>
          </div>
        </div>
      `;
    }

    if (chat.unread == false && chat.sender != me) {
      let div = document.createElement('div');
      div.classList.add('unread-count');
      div.classList.add('bg-dark');
      div.classList.add('rounded-circle');
      //div.innerText = ''
      console.log(a.firstElementChild);
      a.firstElementChild.append(div);
    }
    chat_list.appendChild(a);
  });
};
