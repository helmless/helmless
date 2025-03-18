{{- define "helmless.cloudrun.service.validate" -}}
  {{- include "helmless.cloudrun.validateCPU" . }}
  {{- include "helmless.cloudrun.validateVolumes" . }}
  {{- include "helmless.cloudrun.service.validateProbes" . }}
{{- end -}}

{{/*
Validate probe configuration
*/}}
{{- define "helmless.cloudrun.service.validateProbes" -}}
  {{/* Validate startup probe */}}
  {{- if .Values.startupProbe }}
    {{- if and .Values.startupProbe.timeoutSeconds .Values.startupProbe.periodSeconds }}
      {{- if gt (int .Values.startupProbe.timeoutSeconds) (int .Values.startupProbe.periodSeconds) }}
        {{- fail (printf "timeoutSeconds (%v) cannot exceed periodSeconds (%v)" .Values.startupProbe.timeoutSeconds .Values.startupProbe.periodSeconds) }}
      {{- end }}
    {{- end }}
    {{- if .Values.startupProbe.periodSeconds }}
      {{- if gt (int .Values.startupProbe.periodSeconds) 240 }}
        {{- fail "startupProbe.periodSeconds cannot exceed 240 seconds" }}
      {{- end }}
    {{- end }}
    {{- if and .Values.http2 .Values.startupProbe.httpGet }}
      {{- fail "HTTP probes are not compatible with HTTP/2 (h2c)" }}
    {{- end }}
  {{- end }}

  {{/* Validate liveness probe */}}
  {{- if .Values.livenessProbe }}
    {{- if and .Values.livenessProbe.timeoutSeconds .Values.livenessProbe.periodSeconds }}
      {{- if gt (int .Values.livenessProbe.timeoutSeconds) (int .Values.livenessProbe.periodSeconds) }}
        {{- fail (printf "timeoutSeconds (%v) cannot exceed periodSeconds (%v)" .Values.livenessProbe.timeoutSeconds .Values.livenessProbe.periodSeconds) }}
      {{- end }}
    {{- end }}
    {{- if .Values.livenessProbe.periodSeconds }}
      {{- if gt (int .Values.livenessProbe.periodSeconds) 3600 }}
        {{- fail "livenessProbe.periodSeconds cannot exceed 3600 seconds" }}
      {{- end }}
    {{- end }}
    {{- if and .Values.http2 .Values.livenessProbe.httpGet }}
      {{- fail "HTTP probes are not compatible with HTTP/2 (h2c)" }}
    {{- end }}
    {{- if .Values.livenessProbe.tcpSocket }}
      {{- fail "Liveness probe does not support TCP socket checks" }}
    {{- end }}
  {{- end }}
{{- end }}
