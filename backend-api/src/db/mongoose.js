const mongoose = require('mongoose')

const uri = "mongodb+srv://TarunOP:imfPGjd9ScJvTTGo@cluster0.iseruua.mongodb.net/?retryWrites=true&w=majority";

mongoose.connect(uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})


//imfPGjd9ScJvTTGo TarunOP