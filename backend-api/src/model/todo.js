const mongoose = require('mongoose')

const todoSchema = new mongoose.Schema({
    id: {
        type: String,
    },
    body: {
        type: String,
    },
    status: {
        type: Boolean,
    },
    date: {
        type: Date,
    }
})


const todo = mongoose.model('todo', todoSchema)

module.exports = todo