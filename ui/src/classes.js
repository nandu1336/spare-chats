import store from "./store/index.js";

let date = new Date();

function getTime() {
    return date.toTimeString().split("GMT")[0].trim() + "-" + date.toLocaleDateString();
}

export function makeMessage(content, purpose, to = {}) {
    return new Message(content, purpose, to);
}

class Message {

    constructor(content, purpose, to = {}) {
        this.content = content;
        this.purpose = purpose;
        this.room_code = store.state.roomDetails;
        this.sent_time = getTime();
        this.to = to;
        this.sender = store.state.userDetails;
    }

    as_json() {
        return JSON.stringify(this);
    }
}