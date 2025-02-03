<template>
    <div id="wrapper">
        <div>&nbsp;</div>
        <div id="timer">
            <button type="button" @click="new_game()" class="btn">New Game</button>
            <hr />
            <span id="stats">
                <p>Cards flipped: {{ flipped }}</p>
                <p>Time: {{ time }}</p>
            </span>
        </div>
        <div>&nbsp;</div>
        <div>&nbsp;</div>
        <div id="board">
            <div class="card" v-for="i of cards" v-bind:key='i' :id="i.id">
                <!-- подія @click має бути на елементі з front_view, шоб юзер не міг перевернути вже відкриті карточки -->
                <div class="view front_view"><img src="@/assets/front_view.png" @click='start_point(i)' /></div>
                <div class="view back_view"><img :src="i.vegetable" /></div>
            </div>
        </div>
        <div>&nbsp;</div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            cards: [],
            toggled_cards: [],
            solved: 0,
            flipped: 0,
            time: '00:00',
            total_seconds: 0,
            is_running: false
        }
    },
    methods: {
        makePair() {
            // очистити cards
            this.cards = [];
            // формує карточки для гри
            let vegetables = ["apple.jpg", "broccoli.jpg", "cabbage.jpg", "carrot.jpg", "cherry.jpg", "cucumber.jpg", "pepper.jpg", "pumpkin.jpg", "apple.jpg", "broccoli.jpg", "cabbage.jpg", "carrot.jpg", "cherry.jpg", "cucumber.jpg", "pepper.jpg", "pumpkin.jpg"];
            console.log("makePair()");

            for(const position of Array(16).keys()) {
                let card = {};
                let random_vegetable = Math.floor(Math.random() * vegetables.length);
                
                card.id = position;
                card.vegetable = vegetables[random_vegetable];

                this.cards.push(card);
                vegetables.splice(vegetables.indexOf(vegetables[random_vegetable]), 1);
            }
        },

        new_game() {
            // створити нові карточки
            this.makePair();
            // обнулити кількість перевернутих карточок і таймер
            this.flipped = 0;
            this.is_running = false;
            this.time = "00:00";
            this.total_seconds = 0;
            // якщо гра перезапускається, то це приведе карточки в ісходу позицію
            for(const card of document.getElementsByClassName('front_view')) {
                card.style.display = 'block';
                card.nextElementSibling.style.display = 'none';
            }
        },

        lead_zero(value) {
            if(value < 10) {
                return '0' + value;
            }
            return value;
        },


        toggle_card(card_id) {
            let card = document.getElementById(card_id);
            let front_view = card.getElementsByClassName('front_view')[0];
            let back_view = card.getElementsByClassName('back_view')[0];

            if(front_view.style.display !== 'none') {
                front_view.style.display = 'none';
                back_view.style.display = 'block';
            } else {
                front_view.style.display = 'block';
                back_view.style.display = 'none';
            }
        },

        start_point(card_id) {
            // якщо було відкрито більше ніж 2 карточки, то ігнорувати 
            if(this.toggled_cards.length < 2) {
                this.toggle_card(card_id.id);
                this.toggled_cards.push(card_id);
                this.flipped += 1;
                if (this.is_running == false) {
                    this.is_running = true;
                    this.total_seconds++;
                }
            }
            // якщо вже відкрито дві карточки, то перевірити чи вони співпадають,
            // інакше, закрити по таймауту. В обох випадках очистити масив
            if(this.toggled_cards.length == 2) {
                if(this.toggled_cards[0].vegetable == this.toggled_cards[1].vegetable) {
                    this.solved += 1;
                    if(this.solved == 8) {
                        this.is_running = false;
                        setTimeout(() => { this.new_game() }, 2000);
                        console.log("Game Over");
                    }
                    this.toggled_cards = [];
                } else {
                    setTimeout(() => {
                        // цей костиль потрібний шоб не залишалося зайвих відкритих карточок
                        for(const c of this.toggled_cards) { this.toggle_card(c.id) }
                        this.toggled_cards = [];
                    }, 1000);
                }
            }
        }
    },
    
    watch: {
        total_seconds: {
            handler() {
                if(this.is_running == true) {
                    setTimeout(() => {
                        if(parseInt(this.total_seconds / 60) >= 60) {
                            this.new_game();
                        }

                        this.total_seconds += 1;
                        const minutes = this.lead_zero(parseInt(this.total_seconds / 60));
                        const seconds = this.lead_zero(this.total_seconds % 60);

                        this.time = minutes + ":" + seconds;
                    }, 1000)
                }
            },
        }
    },

    mounted() {
        window.addEventListener("load", this.new_game());
    }
}
</script>

<style>
* {
    background: black;
    color: yellow;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

#timer {
    font-size: 2em;
}

#wrapper {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: 1fr 4fr 1fr;
    grid-auto-columns: minmax(1em);
    grid-auto-rows: minmax(1em);
}

#board {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(4, 1fr);
    grid-gap: 5px;
    margin: 0;
}

button {
    border: 1px solid tomato;
    padding: 10px 15px;
    margin: 10px;
    color: tomato;
    background: black;
}

button:hover {
    border: 1px solid green;
    color: green;
    background: #111;
}

button:active {
    color: tomato;
    background: #555;
}

#stats {
    margin-top: 10px;
    margin-botton: 10px;
}

.view img {
    border: 2px solid blue;
    border-radius: 20px;
    margin-top: 5px;
    width: 128px;
    height: 128px;
}

.front_view {
}

.back_view {
    display: none;
}
</style>
