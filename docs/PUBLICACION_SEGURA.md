# Lista de publicación segura

- [ ] Crear un repositorio **nuevo** usando exclusivamente este paquete público; no subir la carpeta completa V18 privada.
- [ ] Verificar que no haya contraseñas, tokens, service accounts, ADC, `.env`, CSV, `.pbix`, clientes, teléfonos ni direcciones privadas.
- [ ] Inspeccionar rutas y nombres de usuario en scripts y documentación antes de publicar.
- [ ] Si se añaden capturas, confirmar que solo contengan indicadores agregados y que estén autorizadas para divulgación.
- [ ] Revisar permisos/licencias del dataset original antes de publicar extracts o pantallazos basados en datos protegidos.
- [ ] Si se usa Git, revisar **también el historial**; `.gitignore` no elimina secretos ya rastreados.
- [ ] Distinguir claramente la integración opcional con Claude de las alertas reales basadas en reglas.
- [ ] No afirmar que el scheduler local es una operación 24/7.

## Comandos sugeridos (CMD, desde la carpeta de este paquete)

```cmd
git init
git add .
git status
git diff --cached --stat
```

Inspeccionar `git status` antes de hacer commit. Una vez revisado:

```cmd
git commit -m "Document retail intelligence portfolio V18"
```

La creación de un repositorio remoto y su publicación en GitHub son pasos separados y requieren autorización y conexión al servicio.
