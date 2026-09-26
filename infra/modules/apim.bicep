@description('APIM Consumption tier: pay-per-call, no fixed monthly cost, first 1M calls/month free.')
param location string
param namePrefix string
param publisherEmail string
param publisherName string
param backendUrl string

resource apim 'Microsoft.ApiManagement/service@2023-09-01-preview' = {
  name: '${namePrefix}-apim'
  location: location
  sku: {
    name: 'Consumption'
    capacity: 0
  }
  properties: {
    publisherEmail: publisherEmail
    publisherName: publisherName
  }
}

resource api 'Microsoft.ApiManagement/service/apis@2023-09-01-preview' = {
  parent: apim
  name: 'bjjvault-api'
  properties: {
    displayName: 'BJJVault API'
    path: ''
    protocols: ['https']
    serviceUrl: backendUrl
    subscriptionRequired: false
  }
}

resource wildcardOperation 'Microsoft.ApiManagement/service/apis/operations@2023-09-01-preview' = {
  parent: api
  name: 'proxy-all'
  properties: {
    displayName: 'Proxy all'
    method: '*'
    urlTemplate: '/*'
  }
}

output apimGatewayUrl string = apim.properties.gatewayUrl
