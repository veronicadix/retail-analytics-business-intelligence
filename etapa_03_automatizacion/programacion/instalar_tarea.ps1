# V15 - Registrar una tarea semanal interactiva bajo el usuario Windows actual.
# No crea la tarea con SYSTEM, ya que ADC y .env pertenecen al usuario local.
# No ejecuta la carga durante la instalacion.
$ErrorActionPreference = 'Stop'
$nombre = 'Retail_Pipeline_Semanal'
$raiz = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$runner = Join-Path $PSScriptRoot 'ejecutar_semanal.cmd'
$python = Join-Path $raiz '.venv\Scripts\python.exe'
$envFile = Join-Path $raiz '.env'
if (-not (Test-Path $runner)) { throw 'No se encontro ejecutar_semanal.cmd' }
if (-not (Test-Path $python)) { throw 'Primero cree .venv en V15 e instale requirements.txt' }
if (-not (Test-Path $envFile)) { throw 'Primero copie .env de V14 a V15 (no compartirlo)' }
$cuenta = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$accion = New-ScheduledTaskAction -Execute "$env:SystemRoot\System32\cmd.exe" -Argument ('/d /c ""' + $runner + '""') -WorkingDirectory $raiz
# Lunes, 08:00 hora local del equipo (America/Bogota, si el reloj esta configurado correctamente).
$inicio = (Get-Date).Date.AddHours(8)
$disparador = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At $inicio
# Solo cuando este usuario tenga sesion iniciada (necesario para ADC de usuario).
$principal = New-ScheduledTaskPrincipal -UserId $cuenta -LogonType Interactive -RunLevel Limited
# No ejecutar multiples instancias del mismo trabajo; ignorar nuevos disparos.
$ajustes = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 2) -StartWhenAvailable
if (Get-ScheduledTask -TaskName $nombre -ErrorAction SilentlyContinue) {
    throw "Ya existe la tarea '$nombre'. Revisela antes de reemplazarla."
}
Register-ScheduledTask -TaskName $nombre -Action $accion -Trigger $disparador -Principal $principal -Settings $ajustes -Description 'Pipeline retail PostgreSQL a BigQuery Sandbox - lunes 08:00' | Out-Null
Write-Host "Tarea registrada: $nombre"
Write-Host "Usuario: $cuenta"
Write-Host 'Horario: lunes 08:00 (hora local Windows)'
Write-Host "Ruta: $runner"
Write-Host 'No se ejecuto la carga durante esta instalacion.'
