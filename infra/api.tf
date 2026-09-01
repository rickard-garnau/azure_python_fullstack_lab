resource "azurerm_container_app_environment" "env" {
    name = var.project_name
    resource_group_name = azurerm_resource_group.rg.name
    location = azurerm_resource_group.rg.location
}

resource "azurerm_container_app" "api" {
    name = var.project_name
    resource_group_name = azurerm_resource_group.rg.name
    container_app_environment_id = azurerm_container_app_environment.env.id
    revision_mode = "Single"

    secret {
        name  = "acr-password"
        value = azurerm_container_registry.acr.admin_password
}

    registry {
        server                = azurerm_container_registry.acr.login_server
        username               = azurerm_container_registry.acr.admin_username
        password_secret_name   = "acr-password"
}  

    template {
        container {
            name = "api"
            image = "acrrickardgarnau.azurecr.io/backend:${var.image_tag}"
            cpu = 1.0
            memory = "2Gi"
        }
    }

    ingress {
        external_enabled = true
        target_port = 8000
        traffic_weight {
            percentage = 100
            latest_revision = true
        }
    }
}