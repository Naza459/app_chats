const { response } = require('express');
const jwt = require('jsonwebtoken');
const Usuario = require('../models/models');


const validarJWT = async(req, res = response, next) => {

    const token = req.header('x-token');

    if (!token) {
        return res.status(401).json({
            msg: 'No hay token en la petición'
        });
    }

    try {

        const { uid } = jwt.verify(token, process.env.SecretOrPrivateKey);

        const usuario = await Usuario.findById(uid);

        if (!usuario) {
            res.status(401).json({
                msg: 'Token no valido - usuario borrado en la DB'
            })
        }


        // Verificar si el uid tiene estado en True
        if (!usuario.estado) {
            return res.status(401).json({
                msg: 'Token no valido - usuario con el estado en false'
            })
        }


        req.usuario = usuario;

        next();

    } catch (error) {
        console.log(error);
        res.status(401).json({
            msg: 'Token no válido'
        })

    }

}


module.exports = {
    validarJWT
}