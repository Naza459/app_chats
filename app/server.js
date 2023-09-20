const dotenv = require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { dbConnection } = require("../db/config_db");
const { Usuario, Cliente, Conversacion, Catalogo } = require("../models/models");

class Server {
    constructor() {
        this.app = express();
        this.port = process.env.PORT;

        this.paths = {

        }

        // Connect a base de datos
        this.conectarDB();

        
        // Rutas de aplicacion
        //this.routes();
    }

    async conectarDB() {
    await dbConnection();



    // Realiza migraciones o sincronización de modelos aquí
    // await Usuario.sync({alter: true});
    // await Cliente.sync({alter: true});
    // await Conversacion.sync({alter: true});
    // await Catalogo.sync({alter: true});
    }

    routes() {
        //this.app.use(this.paths.auth, require('../routes/auth.js'));
        

    }

    listen() {
        this.app.listen(this.port, () => {
            console.log(`Servidor corriendo en el puerto ${this.port}`)
        });
    }


}

module.exports = Server;