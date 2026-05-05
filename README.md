# IMU_driver_C_STM32

- El objetivo es crear el driver de un sensor IMU, el driver es el que
convierte los datos crudos obtenidos por el sensor en datos utiles, la comunicacion utilizada sera I2C, por lo tanto necesitamos implementar esta comunicacion serial tambien.

***Datos adicionales***
- IDE: VS Code
- Microcontroller: STM32F411RE
- Cross-compiler: arm-none-eabi-gcc
- OS: Linux

- Archivos adicionales: 
    1) core_cm4.h definiciones del procesador ARM
    2) stm32f411xe.h y stm32f411xx.h definiciones del periferico
    3) startup_stm32f411xe.s el hardware siempre busca a la direccion de este archivo, el archivo se encuentra en ensamblador y sus principales tareas son establecer el stack, tabla de vectores, llamar a SystemInit y llamar a main
    4) El linker script.ld es el manual de instruciones para el compilador (indica la cantidad de memoria y variables)
