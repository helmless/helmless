{{/*
Common probe parameters
*/}}
{{- define "helmless.cloudrun.probeParams" -}}
initialDelaySeconds: {{ .probe.initialDelaySeconds | default 0 }}
timeoutSeconds: {{ .probe.timeoutSeconds | default 1 }}
failureThreshold: {{ .probe.failureThreshold | default 3 }}
periodSeconds: {{ .probe.periodSeconds | default 10 }}
{{- end }}

{{/*
HTTP probe configuration
*/}}
{{- define "helmless.cloudrun.httpProbe" -}}
httpGet:
  path: {{ .probe.httpGet.path | quote }}
  port: {{ .probe.httpGet.port | default .containerPort }}
  {{- if .probe.httpGet.httpHeaders }}
  httpHeaders:
    {{- range .probe.httpGet.httpHeaders }}
    - name: {{ .name | quote }}
      value: {{ .value | quote }}
    {{- end }}
  {{- end }}
{{- end }}

{{/*
TCP probe configuration
*/}}
{{- define "helmless.cloudrun.tcpProbe" -}}
tcpSocket:
  port: {{ .probe.tcpSocket.port | default .containerPort }}
{{- end }}

{{/*
gRPC probe configuration
*/}}
{{- define "helmless.cloudrun.grpcProbe" -}}
grpc:
  port: {{ .probe.grpc.port | default .containerPort }}
  {{- if .probe.grpc.service }}
  service: {{ .probe.grpc.service | quote }}
  {{- end }}
{{- end }}

{{/*
Startup probe
*/}}
{{- define "helmless.cloudrun.startupProbe" -}}
{{- if not (hasKey .Values "startupProbe") }}
startupProbe:
  {{- include "helmless.cloudrun.tcpProbe" (dict "probe" (dict "tcpSocket" (dict)) "containerPort" (.Values.containerPort | default 8080)) | nindent 2 }}
  {{- include "helmless.cloudrun.probeParams" (dict "probe" (dict)) | nindent 2 }}
{{- else if .Values.startupProbe }}
startupProbe:
  {{- if .Values.startupProbe.httpGet }}
  {{- include "helmless.cloudrun.httpProbe" (dict "probe" .Values.startupProbe "containerPort" .Values.containerPort) | nindent 2 }}
  {{- end }}
  {{- if .Values.startupProbe.tcpSocket }}
  {{- include "helmless.cloudrun.tcpProbe" (dict "probe" .Values.startupProbe "containerPort" .Values.containerPort) | nindent 2 }}
  {{- end }}
  {{- if .Values.startupProbe.grpc }}
  {{- include "helmless.cloudrun.grpcProbe" (dict "probe" .Values.startupProbe "containerPort" .Values.containerPort) | nindent 2 }}
  {{- end }}
  {{- include "helmless.cloudrun.probeParams" (dict "probe" .Values.startupProbe) | nindent 2 }}
{{- end }}
{{- end }}

{{/*
Liveness probe
*/}}
{{- define "helmless.cloudrun.livenessProbe" -}}
{{- if .Values.livenessProbe }}
livenessProbe:
  {{- if .Values.livenessProbe.httpGet }}
  {{- include "helmless.cloudrun.httpProbe" (dict "probe" .Values.livenessProbe "containerPort" .Values.containerPort) | nindent 2 }}
  {{- end }}
  {{- if .Values.livenessProbe.grpc }}
  {{- include "helmless.cloudrun.grpcProbe" (dict "probe" .Values.livenessProbe "containerPort" .Values.containerPort) | nindent 2 }}
  {{- end }}
  {{- include "helmless.cloudrun.probeParams" (dict "probe" .Values.livenessProbe) | nindent 2 }}
{{- end }}
{{- end }}
