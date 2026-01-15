from django.db import models
from django.urls import reverse

class ObraSocial(models.Model):
    descripcion = models.CharField(max_length=60,verbose_name='Nombre',null=False,blank=False)
    
    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name='Obra Social'
        verbose_name_plural='Obras Sociales'
        ordering = ["descripcion"]


class Persona(models.Model):
    apellido = models.CharField(max_length=60,verbose_name='apellido',null=False,blank=False)
    nombre = models.CharField(max_length=60,verbose_name='nombre',null=False,blank=False)
    direccion = models.CharField(max_length=100,verbose_name='dirección',null=True,blank=True)
    ciudad = models.CharField(max_length=100,verbose_name='localidad',null=True,blank=True)
    mail = models.EmailField(max_length=255,verbose_name='mail',null=True,blank=True)
    tel1 = models.CharField(max_length=25,verbose_name='telefono_1',null=True,blank=True)
    tel2 = models.CharField(max_length=25,verbose_name='telefono_2',null=True,blank=True)
    tel3 = models.CharField(max_length=25,verbose_name='telefono_3',null=True,blank=True)
    obras_sociales = models.ManyToManyField(ObraSocial,verbose_name='Obras Sociales',related_name='personas',blank=True)
    observacion = models.CharField(max_length=250, verbose_name='observaciones', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('persona-detail-view', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s, %s" % (self.apellido,self.nombre)

    class Meta:
        verbose_name='Persona'
        verbose_name_plural='Personas'
        ordering=['apellido','nombre']


class Doctor(models.Model):
    apellido = models.CharField(max_length=60,verbose_name='apellido',null=False,blank=False)
    nombre = models.CharField(max_length=60,verbose_name='nombre',null=False,blank=False)
    ciudad = models.CharField(max_length=60,verbose_name='ciudad',null=False,blank=False)

    def get_absolute_url(self):
        return reverse('doctor-detail-view', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.apellido

    class Meta:
        verbose_name='Doctor'
        verbose_name_plural='Doctores'
        ordering = ['apellido','nombre']


class Lente(models.Model):
    descripcion = models.CharField(max_length=60, verbose_name='Descripción',null=False,blank=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name='Lente'
        verbose_name_plural='Lentes'
        ordering = ["descripcion"]


class Tratamiento(models.Model):
    descripcion = models.CharField(max_length=60, verbose_name='desc_tratamiento',null=False,blank=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name='Tratamiento'
        verbose_name_plural='Tratamientos'
        ordering = ["descripcion"]


class LenteTratamiento(models.Model):
    descripcion = models.CharField(max_length=60, verbose_name='lente_con_tratamiento',null=False,blank=False)
    lente = models.ForeignKey(Lente,null=False,verbose_name='lente',on_delete=models.CASCADE,related_name='lente_lenteTramamiento')
    tratamiento = models.ForeignKey(Tratamiento,null=True,verbose_name='tratamiento',on_delete=models.SET_NULL,related_name='tratamiento_lenteTramamiento')
    
    def __str__(self):
        return self.descripcion
    

    class Meta:
        verbose_name='Lente con Tratamiento'
        verbose_name_plural='Lentes con Tratamiento'


class Proveedor(models.Model):
    descripcion = models.CharField(max_length=60, verbose_name='desc_proveedor',null=False,blank=False)
    # categoria

    class Meta:
        verbose_name='Proveedor'
        verbose_name_plural='Proveedores'
        ordering = ["descripcion"]


class Armazon(models.Model):
    descripcion = models.CharField(max_length=60, verbose_name='desc_armazon',null=False,blank=False)
    proveedor = models.CharField(max_length=60, verbose_name='proveedor_armazon',null=True,blank=True)
    
    def __str__(self):
        return self.descripcion
    

    class Meta:
        verbose_name='Armazon'
        verbose_name_plural='Armazones'
        ordering = ["descripcion"]


class Material(models.Model):
    descripcion = models.CharField(max_length=60, verbose_name='desc_material',null=False,blank=False)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name='Material'
        verbose_name_plural='Materiales'
        ordering = ["descripcion"]
