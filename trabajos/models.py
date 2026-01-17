from django.db import models
from django.urls import reverse
from base.models import Lente, Persona, Doctor, Armazon, ObraSocial, Tratamiento, Material

TIPO_TRABAJO = {
    "MONO": "Monofocal",
    "BI": "Bifocal",
    "MULTI": "Multifocal",
    "1/2": "Ocupacional"
}

TIPO_ANTEOJO = {
    "UNICO": "UNICO",
    "LEJOS": "LEJOS",
    "CERCA": "CERCA",
}

class Trabajo(models.Model):
    # Datos propios del trabajo
    detalle = models.CharField(max_length=250, verbose_name='detalle_trabajo',null=True,blank=True)
    fecha = models.DateTimeField(verbose_name='fecha_trabajo')
    tarea = models.CharField(max_length=250,verbose_name='tarea_trabajo',null=True,blank=True,help_text='Tarea o actividad extra realizada sobre el trabajo')
    tipo_trabajo = models.CharField(max_length=25, choices=TIPO_TRABAJO)
    observacion = models.CharField(max_length=1000,verbose_name='observacion_trabajo',null=True,blank=True)
    # Relaciones de tablas
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, verbose_name='persona', related_name='persona_trabajo')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, verbose_name='doctor',related_name='doctor_trabajo')
    fecha_receta = models.DateField(verbose_name='fecha_receta_trabajo',null=True)
    # lente_con_tratamiento = models.ForeignKey(LenteTratamiento, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='lente_con_tratamiento',related_name='lente_con_tratamiento_trabajo')
    # lente_lejos = models.ForeignKey(Lente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Lente_od', related_name='lente_lejos_trabajo')
    # lente_cerca = models.ForeignKey(Lente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Lente_oi', related_name='lente_cerca_trabajo')
    # tratamiento = models.ForeignKey(Tratamiento, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tratamiento', related_name='tratamiento_trabajo')
    # armazon = models.ForeignKey(Armazon,on_delete=models.SET_NULL,null=True, blank=True, verbose_name='armazon',related_name='armazon_trabajo')
    obra_social = models.ForeignKey(ObraSocial, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='obra_social',related_name='obra_social_trabajo')

    lentes = models.ManyToManyField(Lente, related_name="trabajo_lente", through="TrabajoLente")
    tratamientos = models.ManyToManyField(Tratamiento, related_name="trabajo_tratamiento", through="TrabajoTratamiento")
    armazones = models.ManyToManyField(Armazon, related_name="trabajo_armazon", through="TrabajoArmazon")
    materiales = models.ManyToManyField(Material, related_name="trabajo_material", through="TrabajoMaterial")

    # Detalle de la receta
    od_lejos_esf = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True,verbose_name='ojo_derecho_lejos_esferico')
    od_lejos_cil = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True,verbose_name='ojo_derecho_lejos_cilindrico')
    od_lejos_eje = models.IntegerField(null=True,blank=True,verbose_name='ojo_derecho_lejos_eje')
    od_add = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True,verbose_name='ojo_derecho_adicion')
    od_cerca_esf = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True,verbose_name='ojo_derecho_cerca_esferico')
    od_cerca_cil = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True,verbose_name='ojo_derecho_cerca_cilindrico')
    od_cerca_eje = models.IntegerField(null=True,blank=True,verbose_name='ojo_derecho_cerca_eje')

    oi_lejos_esf = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True,verbose_name='ojo_izquierdo_lejos_esferico')
    oi_lejos_cil = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True,verbose_name='ojo_izquierdo_lejos_cilindrico')
    oi_lejos_eje = models.IntegerField(null=True,blank=True,verbose_name='ojo_izquierdo_lejos_eje')
    oi_add = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True,verbose_name='ojo_izquierdo_adicion')
    oi_cerca_esf = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True,verbose_name='ojo_izquierdo_cerca_esferico')
    oi_cerca_cil = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True,verbose_name='ojo_izquierdo_cerca_cilindrico')
    oi_cerca_eje = models.IntegerField(null=True,blank=True,verbose_name='ojo_izquierdo_cerca_eje')

    def get_absolute_url(self):
        return reverse('trabajo-detail-view', kwargs={'pk': self.pk})

    def __str__(self):
        return (
            f"TRABAJO DE {self.persona.apellido}, {self.persona.nombre} - "
            f"{self.detalle} - FECHA: {self.fecha:%d/%m/%y}"
        )
    
    def get_tipo_trabajo(self):
        return TIPO_TRABAJO

    def get_tipo_anteojo(self):
        return TIPO_ANTEOJO

    @property
    def lente_unico(self):
        return (
            self.TrabajoLente_trabajo
            .select_related("lente")
            .filter(tipo="UNICO")
            .first()
        )
        
    @property
    def lente_lejos(self):
        return (
            self.TrabajoLente_trabajo
            .select_related("lente")
            .filter(tipo="LEJOS")
            .first()
        )
        
    @property
    def lente_cerca(self):
        return (
            self.TrabajoLente_trabajo
            .select_related("lente")
            .filter(tipo="CERCA")
            .first()
        )

    @property
    def tratamiento_unico(self):
        return (
            self.TrabajoTratamiento_trabajo
            .select_related("tratamiento")
            .filter(tipo="UNICO")
            .first()
        )
        
    @property
    def tratamiento_lejos(self):
        return (
            self.TrabajoTratamiento_trabajo
            .select_related("tratamiento")
            .filter(tipo="LEJOS")
            .first()
        )
        
    @property
    def tratamiento_cerca(self):
        return (
            self.TrabajoTratamiento_trabajo
            .select_related("tratamiento")
            .filter(tipo="CERCA")
            .first()
        )
    
    @property
    def armazon_unico(self):
        return (
            self.TrabajoArmazon_trabajo
            .select_related("armazon")
            .filter(tipo="UNICO")
            .first()
        )
        
    @property
    def armazon_lejos(self):
        return (
            self.TrabajoArmazon_trabajo
            .select_related("armazon")
            .filter(tipo="LEJOS")
            .first()
        )
        
    @property
    def armazon_cerca(self):
        return (
            self.TrabajoArmazon_trabajo
            .select_related("armazon")
            .filter(tipo="CERCA")
            .first()
        )
    
    @property
    def material_unico(self):
        return (
            self.TrabajoMaterial_trabajo
            .select_related("material")
            .filter(tipo="UNICO")
            .first()
        )
        
    @property
    def material_lejos(self):
        return (
            self.TrabajoMaterial_trabajo
            .select_related("material")
            .filter(tipo="LEJOS")
            .first()
        )
        
    @property
    def material_cerca(self):
        return (
            self.TrabajoMaterial_trabajo
            .select_related("material")
            .filter(tipo="CERCA")
            .first()
        )

    class Meta:
        verbose_name='Trabajo'
        verbose_name_plural='Trabajos'


class TrabajoLente(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.RESTRICT, related_name="TrabajoLente_trabajo", null=False)
    lente = models.ForeignKey(Lente, on_delete=models.RESTRICT, related_name="TrabajoLente_lente", null=False)
    tipo = models.CharField(max_length=25, choices=TIPO_ANTEOJO, null=False, blank=False, verbose_name="tipo_lente")


class TrabajoTratamiento(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.RESTRICT, related_name="TrabajoTratamiento_trabajo", null=False)
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.RESTRICT, related_name="TrabajoTratamiento_tratamiento", null=False)
    tipo = models.CharField(max_length=25, choices=TIPO_ANTEOJO, null=False, blank=False)


class TrabajoArmazon(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.RESTRICT, related_name="TrabajoArmazon_trabajo", null=False)
    armazon = models.ForeignKey(Armazon, on_delete=models.RESTRICT, related_name="TrabajoArmazon_armazon", null=False)
    tipo = models.CharField(max_length=25, choices=TIPO_ANTEOJO, null=False, blank=False)


class TrabajoMaterial(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.RESTRICT, related_name="TrabajoMaterial_trabajo", null=False)
    material = models.ForeignKey(Material, on_delete=models.RESTRICT, related_name="TrabajoMaterial_armazon", null=False)
    tipo = models.CharField(max_length=25, choices=TIPO_ANTEOJO, null=False, blank=False)
