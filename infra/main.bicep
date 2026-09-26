@description('Deployment location.')
param location string = resourceGroup().location

@description('Short name prefix for all resources, e.g. "bjjvault-dev".')
param namePrefix string = 'bjjvault-dev'

param sqlAdminLogin string
@secure()
param sqlAdminPassword string

param apimPublisherEmail string
param apimPublisherName string = 'BJJVault'

@description('Public URL of the AKS ingress/service that APIM should forward to. Set after the AKS ingress is provisioned.')
param backendUrl string = 'https://placeholder.invalid'

module acr 'modules/acr.bicep' = {
  name: 'acr'
  params: {
    location: location
    namePrefix: namePrefix
  }
}

module monitoring 'modules/monitoring.bicep' = {
  name: 'monitoring'
  params: {
    location: location
    namePrefix: namePrefix
  }
}

module sql 'modules/sql.bicep' = {
  name: 'sql'
  params: {
    location: location
    namePrefix: namePrefix
    sqlAdminLogin: sqlAdminLogin
    sqlAdminPassword: sqlAdminPassword
  }
}

module aks 'modules/aks.bicep' = {
  name: 'aks'
  params: {
    location: location
    namePrefix: namePrefix
    logAnalyticsWorkspaceId: monitoring.outputs.logAnalyticsId
    acrId: acr.outputs.acrId
  }
}

module apim 'modules/apim.bicep' = {
  name: 'apim'
  params: {
    location: location
    namePrefix: namePrefix
    publisherEmail: apimPublisherEmail
    publisherName: apimPublisherName
    backendUrl: backendUrl
  }
}

module staticWebApp 'modules/staticwebapp.bicep' = {
  name: 'staticwebapp'
  params: {
    location: location
    namePrefix: namePrefix
  }
}

output acrLoginServer string = acr.outputs.loginServer
output aksName string = aks.outputs.aksName
output sqlServerFqdn string = sql.outputs.sqlServerFqdn
output sqlDatabaseName string = sql.outputs.sqlDatabaseName
output apimGatewayUrl string = apim.outputs.apimGatewayUrl
output staticWebAppHostname string = staticWebApp.outputs.defaultHostname
output appInsightsConnectionString string = monitoring.outputs.appInsightsConnectionString
