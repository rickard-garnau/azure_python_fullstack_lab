variable "resource_group_name" {
  default = "FastlyDep"
  type    = string
}

variable "location" {
  type    = string
  default = "swedencentral"
}

variable "project_name" {
  default = "fastlydep"
}

variable "acr_name" {
  default = "acrrickardgarnau"
}

variable "image_tag" {
  default = "latest"
}

variable "tags" {
  type = map(string)
  default = {
    environment = "dev"
    project     = "eclipsebord"
    owner       = "rickard garnau"
  }
}
