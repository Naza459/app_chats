const { response, request } = require('express');
const Usuario = require("../models/models");
const bcryptjs = require("bcryptjs");



const usuariosGet = async(req = request, res = response) => {

    const { limite = 5, desde = 0 } = req.query;
    const query = { estado: true }

    const [total, usuarios] = await Promise.all([
        Usuario.countDocuments(query),
        Usuario.find(query)
        .skip(Number(desde))
        .limit(Number(limite))
    ])

    res.json({
        usuarios,
        total
    });
};

const usuariosPost = async(req, res = response) => {


    const { name, username, email, password, rol } = req.body;
    const usuario = new Usuario({ name, username, email, password, rol });

    // Verificar si el correo existe

    // Encriptar la contraseña
    const salt = bcryptjs.genSaltSync();
    usuario.password = bcryptjs.hashSync(password, salt);

    // Guardar en DB
    await usuario.save();

    res.status(200).json({
        msg: 'POST API - Controller',
        usuario
    });
};

const usuariosPut = async(req, res = response) => {

    const id = req.params.id;
    const { _id, password, correo, ...resto } = req.body;

    // TODO validar contra base de datos.
    if (password) {
        const salt = bcryptjs.genSaltSync();
        resto.password = bcryptjs.hashSync(password, salt);
    }

    const usuario = await Usuario.findByIdAndUpdate(id, resto)

    res.json(usuario);
};
const usuariosDelete = async(req, res = response) => {

    const { id } = req.params;

    //Fisicamente lo borramos
    // const usuario = await Usuario.findByIdAndDelete(id);
    const usuario = await Usuario.findByIdAndUpdate(id, { estado: true });

    res.json({
        //id,
        usuario
    });

};




module.exports = {
    usuariosGet,
    usuariosPost,
    usuariosPut,
    usuariosDelete
};