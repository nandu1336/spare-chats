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
        this.room_code = store.state.roomDetails.room_code;
        this.content = content;
        this.sender = store.state.userDetails;
        this.sent_time = getTime();
        this.purpose = purpose;
        this.to = to;
    }

    as_json() {
        return JSON.stringify(this);
    }
}