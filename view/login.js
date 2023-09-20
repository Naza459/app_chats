const { response, json } = require("express");
const { Usuario, Cliente, Conversacion, Catalogo } = require("../models/models");
const bcrypt = require('bcryptjs');

const login = async(req, res = response) => {


    const { email,username, password } = req.body;

    try {

        // Verificar si el email existe
        const usuario = await Usuario.findOne({ email });
        if (!usuario) {
            return res.status(400).json({
                msg: 'El usuario / Password no son correctos - Correo'
            })
        }


        // Si el usuario esta activo
        if (!usuario.estado) {
            return res.status(400).json({
                msg: 'Usuario / Password no son correctos - Estado: false'
            })
        }

        // Verificar la contraseña
        const validarPassword = bcryptjs.compareSync(password, usuario.password);
        if (!validarPassword) {
            return res.status(400).json({
                msg: 'Usuario / Password no son correctos - Password'
            })
        }

        // Generar el JWT
        const token = await generarJWT(usuario.id);

        res.json({
            usuario,
            token,
        })

    } catch (error) {
        res.status(500).json({
            msg: 'Error, Algo salio mal!',
        });
    }
}