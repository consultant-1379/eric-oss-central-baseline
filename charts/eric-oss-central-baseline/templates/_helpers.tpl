{{/* vim: set filetype=mustache: */}}

{{/*
Expand the name of the chart.
*/}}
{{- define "eric-oss-central-baseline.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Expand the name of an external service.
*/}}
{{- define "eric-oss-central-baseline.service.name" -}}
{{- .nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Expand the chart name.
*/}}
{{- define "eric-oss-central-baseline.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create image pull secrets
*/}}
{{- define "eric-oss-central-baseline.pullSecrets" -}}
{{- if .Values.imageCredentials.registry -}}
{{- if .Values.imageCredentials.registry.pullSecret -}}
{{- print .Values.imageCredentials.registry.pullSecret -}}
{{- else if .Values.global.registry.pullSecret -}}
{{- print .Values.global.registry.pullSecret -}}
{{- else -}}
""
{{- end -}}
{{- else if .Values.global.registry.pullSecret -}}
{{- print .Values.global.registry.pullSecret -}}
{{- else -}}
""
{{- end -}}
{{- end -}}

{{- define "eric-oss-central-baseline.product-info" }}
ericsson.com/product-name: "SON Common Package"
ericsson.com/product-number: "CXP 903 6949/1"
ericsson.com/product-revision: "{{.Values.productInfo.rstate}}"
{{- end}}
