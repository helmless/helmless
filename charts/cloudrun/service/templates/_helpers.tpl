{{/*
Expand the name of the chart.
*/}}
{{- define "serverless-helm.cloudrun.name" -}}
{{- default .Values.name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create the fully qualified image name.
*/}}
{{- define "helmless.image" -}}
{{- if typeIs "string" .Values.image }}
{{- .Values.image }}
{{- else }}
{{- if .Values.image.registry }}
{{- printf "%s/%s" .Values.image.registry .Values.image.repository }}
{{- else }}
{{- printf "%s" .Values.image.repository }}
{{- end }}
{{- if .Values.image.name }}
{{- printf "/%s" .Values.image.name }}
{{- end }}
{{- if .Values.image.tag }}
{{- printf ":%s" .Values.image.tag }}
{{- end }}
{{- end }}
{{- end }}

{{/*
The container port.
*/}}
{{- define "serverless-helm.cloudrun.containerPort" -}}
{{- default 8080 .Values.containerPort | int }}
{{- end }}

{{/*
Sanitizes and formats an env variable to conform with the CloudRun spec.
*/}}
{{- define "serverless-helm.cloudrun.env" -}}
{{/*
Helper to map environment variables and secrets to a envVars list.
*/}}
{{- with .Values.env }}
{{- range $key, $value := . }}
{{- if $value }}
- name: {{ $key | quote }}
  value: {{ $value | quote }}
{{- end }}
{{- end }}
{{- end }}
{{- end }}


{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "serverless-helm.cloudrun.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "serverless-helm.cloudrun.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "serverless-helm.cloudrun.labels" -}}
helm.sh/chart: {{ include "serverless-helm.cloudrun.chart" . }}
{{ include "serverless-helm.cloudrun.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "serverless-helm.cloudrun.selectorLabels" -}}
app.kubernetes.io/name: {{ include "serverless-helm.cloudrun.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "serverless-helm.cloudrun.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "serverless-helm.cloudrun.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
