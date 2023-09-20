const { Router } = require('express');
const { check } = require('express-validator');
const {usuariosGet} = require('../view//user')
const { validarCampos, validarJWT } = require('../middleware/')

const router = new Router();

router.get("/", usuariosGet);

router.post(
    "/", [
        check("username", "El nombre es obligatorio").notEmpty(),
        check("password", "El password debe ser mas de 6 letras").isLength({
            min: 6,
        }),
        //check("correo", "El correo no es valido").isEmail(),
        //check("email").custom(esCorreoValido),
        //check("rol", "No es un rol valido").isIn(["ADMIN_ROLE", "USER_ROLE"]),
        //check("rol").custom(esRoleValido),
        validarCampos,
    ],
    usuariosPost
);