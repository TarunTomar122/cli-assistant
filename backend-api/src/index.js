const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')

require('./db/mongoose')

const todo = require('./model/todo')

const PORT = process.env.PORT || 4000

app = express()

app.use(cors());
app.use(bodyParser.urlencoded({ extended: true }))

var today = new Date();

app.post('/add_todo', bodyParser.json(), async (req, res) => {

    const todoObj = new todo({ id: Math.random().toString(16).substr(2, 4), body: req.body.body, status: false, date: new Date(today.toDateString() + ' ' + '23:00') })
    try {
        await todoObj.save()
        res.send({ "error": null, "message": "todo Saved Successfully" })
    } catch (er) {
        console.log("Error while saving a todo", er);
        res.send({ "error": er, "message": "Error while saving a todo" })
    }

})

app.post('/get_todos', bodyParser.json(), async (req, res) => {

    let timeframe = req.body.timeframe;
    if (timeframe == "now" || timeframe == "today") {
        // fetch todos having date as today
        todo.find({ date: new Date(today.toDateString() + ' ' + '23:00') }, async (er, result) => {
            if (er) {
                console.log("something went wrong while fetching todos", er);
                res.send({ 'error': er, "message": "Error while fetching todos" })
            } else {
                res.send({ 'error': null, "message": result })
            }
        })

    } else if (timeframe == "future") {
        // fetch all future todos 
        todo.find({ date: { $gte: new Date(today.toDateString() + ' ' + '23:00') } }, async (er, result) => {
            if (er) {
                console.log("something went wrong while fetching todos", er);
                res.send({ 'error': er, "message": "Error while fetching todos" })
            } else {
                res.send({ 'error': null, "message": result })
            }
        })
    } else {
        // fetch todos for this particular day
        todo.find({ date: new Date(timeframe + ' ' + '23:00') }, async (er, result) => {
            if (er) {
                console.log("something went wrong while fetching todos", er);
                res.send({ 'error': er, "message": "Error while fetching todos" })
            } else {
                res.send({ 'error': null, "message": result })
            }
        })
    }

})

app.post("/mark_todo", bodyParser.json(), async (req, res) => {

    let id = req.body.id;
    await todo.findOneAndUpdate({ id }, { status: true });

    todo.find({ date: new Date(today.toDateString() + ' ' + '23:00') }, async (er, result) => {
        if (er) {
            console.log("something went wrong while fetching todos", er);
            res.send({ 'error': er, "message": "Error while fetching todos" })
        } else {
            res.send({ 'error': null, "message": result })
        }
    })

})

const server = app.listen(PORT, () => {
    console.log("Server is Up and Running On Port: ", PORT)
})
