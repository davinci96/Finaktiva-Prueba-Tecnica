# Prueba Técnica

Repositorio que contiene prueba técnica para el cargo de LIDER DE INFRAESTRUCTURA

## Calculadora de Costos

[Calculadora de AWS](https://calculator.aws/#/estimate?id=d8d8b6e37e2b04aabadacc96d112770fba3cb560)


## Explicación del Pipeline y la Infraestructura

Este proyecto consta de dos partes:

### 1. Pipelines

El repositorio contiene dos pipeline en la carpeta `.github/workflows/` uno DeployInfra.yml y otro Deployapp.yml, realizado con GitHub Actions. Se divide en dos pasos:

#### 1.1 Pipeline DeployInfra.yml
DeployDEV
- Instala Node y python
- Configura AWS Credentials.
- Carga y exporta las variables del arvhivo env_params.json
- Instala dependencias para CDK y otras herramientas.
- Instala Checkov para vulnerabilidades en la IAC
- Bootstrap CDK para preparar el entorno.
- Despliega la infraestructura (VPC, ECR)
- Construye, etiqueta y sube imágenes Docker a Amazon ECR.

#### 1.2 
Deploy-Ecs-Elb

- Los mismo pasos del DeployDev
- Despliega el ECS Stack, ALB y un Monitor de CloudWatch en el entorno de AWS, después de que DeployDEV se haya completado.

Se usa una estrategia de despliegue secuencial. Primero, se despliega la infraestructura base (VPC, repositorios de ECR, etc.), y luego, en un paso separado, se despliegan los servicios en ECS, ALB y CloudWatch que dependen de esa infraestructura.

#### 1.3 Pipeline Deployapp.yml
 trivy-scan
- Instala Trivy
- Escanea los dos Dockerfile para encontrar vulnerabilidades

#### 1.3 
 deploy
- Instala jq
- Configura AWS Credentials.
- Se loguea en AWS ECR
- Construye, etiqueta y sube las imagenes a ECR
- Actualiza los servicios, actualizando las dos task definitions con las nuevas imagenes

#### 1.4 
 rollback
 Este job solo se ejecuta manual, por si se tiene que devolver a la version anterior por algun cambio no requerido
- Instala jq
- Hace un rollback de los services devolviendose a la anterior task definition

### 2. Infraestructura como Código (IaC)

La infraestructura se encuentra en la ruta `infra` y utiliza AWS Cloud Development Kit (CDK). La infraestructura incluye:

- **VPC (Virtual Private Cloud)**

  Archivo: `vpc_stack.py`

  Define una VPC con subredes públicas y privadas. Utiliza un archivo de parámetros (`env_params.json`) para definir el CIDR y otros parámetros importantes.

- **ECS (Elastic Container Service)**

  Archivo: `ecs_stack.py`

  Crea un clúster de ECS con servicios Fargate. Incluye autoescalado de tareas basado en la utilización de CPU.

- **ECR (Elastic Container Registry)**

  Archivos: `ecr_stack.py`

  Define dos repositorios de ECR para almacenar imágenes de contenedor, configurados con reglas de ciclo de vida para mantener solo las imágenes etiquetadas como 'latest'.

- **ELB (Elastic Load Balancer)**

  Archivo: `alb_stack.py`

  Configura un Application Load Balancers (ALB) para los servicios ECS. El ALB escucha en el puerto 80 (HTTP) y redirige el tráfico a los servicios ECS.

- **CloudWatch**

  Archivo: `cloudwatch_stack.py`

  Define una pila de AWS CDK para monitorear un servicio ECS utilizando CloudWatch. Incluye una métrica para el uso de CPU y una alarma que se activa si el uso supera el 70% durante dos períodos consecutivos.

### Cómo Ejecutar

#### Localmente

1. **Configuración Inicial:**

   Asegúrate de tener AWS CLI y AWS CDK instalados y configurados.

2. **Bootstrap:**

   Ejecuta `cdk bootstrap` para inicializar los recursos necesarios en tu cuenta de AWS.

3. **Despliegue:**

   Ejecuta `cdk deploy` o `cdk deploy VpcStack`, `cdk deploy EcrStack`, etc., para desplegar la infraestructura.

#### Automáticamente

El pipeline se ejecuta automáticamente cuando se hace un commit en las ramas `develop`, `release` o `main`. El agente tiene los paquetes y librerías necesarios. La región de despliegue depende de la rama:

- `main`: us-east-2
- `release`: us-west-2
- `develop`: us-east-1

#### Requisitos

- AWS CLI
- AWS CDK
- Node.js
- Python 3.12

Además, crea secretos en Repository secrets para que el pipeline funcione correctamente:

- `AWS_ACCOUNT_ID`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- 'AWS_ACCOUNT_ID'
- 'AWS_ECR_CONTEXTS'
- 'AWS_ECR_DOCKERFILES'
- 'AWS_ECR_IMAGE_TAGS'
- 'AWS_ECR_REPOSITORY_NAME'
- 'AWS_ECS_CLUSTER'
- 'AWS_ECS_SERVICE_NAMES'
- 'AWS_ECS_TASK_DEFINITIONS'

  ## Diagrama de Arquitectura

![Finaktiva drawio (1)](https://github.com/user-attachments/assets/a4140f12-1056-4874-8c74-70bb9e1150ab)




